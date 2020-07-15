import pytest
import flask_sse
import redis
import types
import flask

pytestmark = pytest.mark.usefixtures("appctx")


@pytest.fixture
def bp(app):
    _bp = flask_sse.ServerSentEventsBlueprint('test-sse', __name__)
    app.register_blueprint(_bp, url_prefix='/stream')
    return _bp


def test_no_redis_configured(bp):
    with pytest.raises(KeyError) as excinfo:
        bp.redis

    expected = 'Must set a redis connection URL in app config.'
    assert str(excinfo.value.args[0]) == expected


def test_redis_url_config(bp, app):
    app.config["REDIS_URL"] = "redis://localhost"
    assert isinstance(bp.redis, redis.StrictRedis)
    assert bp.redis.connection_pool.connection_kwargs['host'] == 'localhost'


def test_sse_redis_url_config(bp, app):
    app.config["SSE_REDIS_URL"] = "redis://localhost"
    assert isinstance(bp.redis, redis.StrictRedis)
    assert bp.redis.connection_pool.connection_kwargs['host'] == 'localhost'


def test_config_priority(bp, app):
    app.config["REDIS_URL"] = "redis://1.1.1.1"
    app.config["SSE_REDIS_URL"] = "redis://2.2.2.2"
    assert isinstance(bp.redis, redis.StrictRedis)
    assert bp.redis.connection_pool.connection_kwargs['host'] == '2.2.2.2'


def test_publish_nothing(bp, app):
    app.config["SSE_REDIS_URL"] = "redis://localhost"
    with pytest.raises(TypeError):
        bp.publish()


def test_publish(bp, app, mockredis):
    app.config["SSE_REDIS_URL"] = "redis://localhost"
    bp.publish("thing")
    mockredis.publish.assert_called_with(channel='sse', message='{"data": "thing"}')


def test_publish_channel(bp, app, mockredis):
    app.config["SSE_REDIS_URL"] = "redis://localhost"
    bp.publish("thing", channel='garden')
    mockredis.publish.assert_called_with(channel='garden', message='{"data": "thing"}')


def test_publish_type(bp, app, mockredis):
    app.config["SSE_REDIS_URL"] = "redis://localhost"
    bp.publish("thing", type='example')
    mockredis.publish.assert_called_with(
        channel='sse',
        message='{"data": "thing", "type": "example"}',
    )


def test_messages(bp, app, mockredis):
    app.config["SSE_REDIS_URL"] = "redis://localhost"
    pubsub = mockredis.pubsub.return_value
    pubsub.listen.return_value = [
        {
            "type": "message",
            "data": '{"data": "thing", "type": "example"}',
        }
    ]

    gen = bp.messages()

    assert isinstance(gen, types.GeneratorType)
    output = list(gen)
    assert output == [flask_sse.Message("thing", type="example")]
    pubsub.subscribe.assert_called_with('sse')
    pubsub.unsubscribe.assert_called_with('sse')


def test_messages_channel(bp, app, mockredis):
    app.config["SSE_REDIS_URL"] = "redis://localhost"
    pubsub = mockredis.pubsub.return_value
    pubsub.listen.return_value = [
        {
            "type": "message",
            "data": '{"data": "whee", "id": "abc"}',
        }
    ]
    pubsub.unsubscribe.side_effect = redis.exceptions.ConnectionError()

    gen = bp.messages('whee')

    assert isinstance(gen, types.GeneratorType)
    output = list(gen)
    assert output == [flask_sse.Message("whee", id="abc")]
    pubsub.subscribe.assert_called_with('whee')
    pubsub.unsubscribe.assert_called_with('whee')


def test_messages_close(bp, app, mockredis):
    app.config["SSE_REDIS_URL"] = "redis://localhost"
    pubsub = mockredis.pubsub.return_value
    pubsub.listen.return_value = [
        {
            "type": "message",
            "data": '{"data": "whee", "id": "abc"}',
        }
    ]

    gen = bp.messages('whee')

    assert isinstance(gen, types.GeneratorType)
    output = next(gen)
    assert output == flask_sse.Message("whee", id="abc")
    pubsub.subscribe.assert_called_with('whee')
    pubsub.unsubscribe.assert_not_called()
    gen.close()
    pubsub.unsubscribe.assert_called_with('whee')


def test_stream(bp, app, mockredis):
    app.config["SSE_REDIS_URL"] = "redis://localhost"
    pubsub = mockredis.pubsub.return_value
    pubsub.listen.return_value = [
        {
            "type": "message",
            "data": '{"data": "thing", "type": "example"}',
        }
    ]

    resp = bp.stream()

    assert isinstance(resp, flask.Response)
    assert resp.mimetype == "text/event-stream"
    assert resp.is_streamed
    output = resp.get_data(as_text=True)
    assert output == "event:example\ndata:thing\n\n"
    pubsub.subscribe.assert_called_with('sse')


def test_sse_object():
    assert isinstance(flask_sse.sse, flask_sse.ServerSentEventsBlueprint)
    # calling `add_url_rule` adds an entry to the `deferred_functions` list,
    # which is about the only thing we can test for
    assert len(flask_sse.sse.deferred_functions) == 1


def test_stream_channel_arg(app, mockredis):
    app.config["REDIS_URL"] = "redis://localhost"
    app.register_blueprint(flask_sse.sse, url_prefix='/stream')
    client = app.test_client()
    pubsub = mockredis.pubsub.return_value
    pubsub.listen.return_value = [
        {
            "type": "message",
            "data": '{"data": "thing", "type": "example"}',
        }
    ]

    resp = client.get("/stream?channel=different")

    assert isinstance(resp, flask.Response)
    assert resp.mimetype == "text/event-stream"
    assert resp.is_streamed
    output = resp.get_data(as_text=True)
    assert output == "event:example\ndata:thing\n\n"
    pubsub.subscribe.assert_called_with('different')
