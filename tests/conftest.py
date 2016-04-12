import pytest
from flask import Flask
from mockredis import mock_strict_redis_client


@pytest.fixture
def app():
    _app = Flask(__name__)
    _app.secret_key = "anything"
    _app.testing = True

    @_app.route("/")
    def index():
        return "index"

    return _app


@pytest.yield_fixture
def appctx(app):
    with app.test_request_context("/") as ctx:
        yield ctx

@pytest.fixture
def mockredis(mocker):
    _mr = mocker.Mock(name="mockredis")
    mocker.patch("flask_sse.StrictRedis", return_value=_mr)
    mocker.patch("flask_sse.StrictRedis.from_url", return_value=_mr)
    return _mr
