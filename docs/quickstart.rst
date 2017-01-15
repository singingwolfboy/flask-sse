Quickstart
==========

Here's a quick working example of how Flask-SSE works.

.. warning::
   `Server-sent events`_ do *not* work with Flask's built-in development server,
   because it handles HTTP requests one at a time. The SSE stream is intended
   to be an infinite stream of events, so it will never complete. If you try
   to run this code on with the built-in development server, the server will
   be unable to take any other requests once you connect to this stream.
   Instead, you must use a web server with asychronous workers. Gunicorn_
   can work with gevent_ to use asychronous workers: see :ref:`gunicorn's
   design documentation <gunicorn:design>`.

   You will also need a Redis_ server running locally for this example to work.

Make a virtual environment and install Flask-SSE, ``gunicorn``, and ``gevent``.
You will also need to make sure you have a Redis_ server running locally.

.. code-block:: bash

    $ pyvenv sse
    $ pip install flask-sse gunicorn gevent

Make a file on your computer called ``sse.py``, with the following content:

.. code-block:: python

    from flask import Flask, render_template
    from flask_sse import sse

    app = Flask(__name__)
    app.config["REDIS_URL"] = "redis://localhost"
    app.register_blueprint(sse, url_prefix='/stream')

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/hello')
    def publish_hello():
        sse.publish({"message": "Hello!"}, type='greeting')
        return "Message sent!"

If you are using a Redis server that has a password use::

    app.config["REDIS_URL"] = "redis://:password@localhost"

Make a ``templates`` folder next to ``sse.py``, and create a file named
``index.html`` in that folder, with the following content:

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
      <title>Flask-SSE Quickstart</title>
    </head>
    <body>
      <h1>Flask-SSE Quickstart</h1>
      <script>
        var source = new EventSource("{{ url_for('sse.stream') }}");
        source.addEventListener('greeting', function(event) {
            var data = JSON.parse(event.data);
            alert("The server says " + data.message);
        }, false);
        source.addEventListener('error', function(event) {
            alert("Failed to connect to event stream. Is Redis running?");
        }, false);
      </script>
    </body>
    </html>

Run your code using gunicorn's gevent workers:

.. code-block:: bash

    $ gunicorn sse:app --worker-class gevent --bind 127.0.0.1:8000

Open your web browser, and visit ``127.0.0.1:8000``. Your web browser will
automatically connect to the server-sent event stream. Open another tab, and
visit ``127.0.0.1:8000/hello``. You should get a Javascript alert in the first
tab when you do so.

.. _Server-sent events: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
.. _Redis: http://www.redis.io/
.. _gunicorn: http://gunicorn.org/
.. _gevent: http://www.gevent.org/
