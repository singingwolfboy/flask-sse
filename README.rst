Flask SSE |build-status| |coverage-status| |docs|
=================================================
A Flask extension for HTML5 `server-sent events`_ support, powered by Redis_.

Example of sending events:

.. code-block:: python

    from flask import Flask
    from flask_sse import sse

    app = Flask(__name__)
    app.config["REDIS_URL"] = "redis://localhost"
    app.register_blueprint(sse, url_prefix='/stream')

    @app.route('/send')
    def send_message():
        sse.publish({"message": "Hello!"}, type='greeting')
        return "Message sent!"

To receive events on a webpage, use Javascript to connect to the event stream,
like this:

.. code-block:: javascript

    var source = new EventSource("{{ url_for('sse.stream') }}");
    source.addEventListener('greeting', function(event) {
        var data = JSON.parse(event.data);
        // do what you want with this data
    }, false);

`The full documentation for this project
is hosted on ReadTheDocs. <http://flask-sse.readthedocs.org/>`_

.. _server-sent events: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
.. _Redis: http://www.redis.io/

.. |build-status| image:: https://travis-ci.org/singingwolfboy/flask-sse.svg?branch=master&style=flat
   :target: https://travis-ci.org/singingwolfboy/flask-sse
   :alt: Build status
.. |coverage-status| image:: http://codecov.io/github/singingwolfboy/flask-sse/coverage.svg?branch=master
   :target: http://codecov.io/github/singingwolfboy/flask-sse?branch=master
   :alt: Test coverage
.. |docs| image:: https://readthedocs.org/projects/flask-sse/badge/?version=latest&style=flat
   :target: http://flask-sse.readthedocs.org/
   :alt: Documentation
