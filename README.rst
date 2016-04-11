Flask SSE
=========
A Flask extension for HTML5 `server-sent events`_ support, powered by Redis_.

Example of sending events:

.. code-block:: python

    from flask import Flask, json
    from flask_sse import sse

    app = Flask(__name__)
    app.config["REDIS_URL"] = "redis://localhost"
    app.register_blueprint(sse, url_prefix='/stream')

    @app.route('/send')
    def send_message():
        sse.publish('event-type', {"message": "Hello!"})
        return "Message sent!"

To receive events on a webpage, use Javascript to connect to the event stream,
like this:

.. code-block:: javascript

    var source = new EventSource("{{ url_for('sse.stream') }}");
    source.addEventListener('event-type', function(event) {
        var data = JSON.parse(event.data);
        // do what you want with this data
    }, false);

.. _server-sent events: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
.. _Redis: http://www.redis.io/
