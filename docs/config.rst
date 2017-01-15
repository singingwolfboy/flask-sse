Configuration
=============

Redis
-----

In order to use Flask-SSE, you need a Redis_ server to handle pubsub_.
Flask-SSE will search the :ref:`application config <flask:config>` for a Redis
connection URL to use. It will try the following configuration values, in
order:

1. ``SSE_REDIS_URL``
2. ``REDIS_URL``

If it doesn't find a Redis connection URL, Flask-SSE will raise a
:exc:`KeyError` any time a client tries to access the SSE stream, or any time
an event is published.

We recommend that you set this connection URL in an environment variable,
and then load it into your application configuration using :data:`os.environ`,
like this:

.. code-block:: python

    import os
    from flask import Flask

    app = Flask(__name__)
    app.config["REDIS_URL"] = os.environ.get("REDIS_URL")

If you are using a Redis server that has a password use::

    app.config["REDIS_URL"] = "redis://:password@localhost"

Application Server
------------------

Flask-SSE does *not* work with Flask's built-in development server, due to
the nature of the `server-sent events`_ protocol. This protocol uses long-lived
HTTP requests to push data from the server to the client, which means that an
HTTP request to the event stream will effectively never complete. Flask's
built-in development server is single threaded, so it can only handle one HTTP
request at a time. Once a client connects to the event stream, it will not
be able to make any other HTTP requests to your site.

Instead, you must use a web server with asychronous workers. Asynchronous
workers allow one worker to continuously handle the long-lived HTTP request
that server-sent events require, while other workers simultaneously handle
other HTTP requests to the server. Gunicorn_ is an excellent choice for an
application server, since it can work with gevent_ to use asychronous workers:
see :ref:`gunicorn's design documentation <gunicorn:design>`.

For further information, see
:ref:`Flask's deployment documentation <flask:deployment>`.
Note that Flask's development server should **never** be used for deployment,
regardless of whether you use Flask-SSE.

.. _Redis: http://www.redis.io/
.. _pubsub: http://redis.io/topics/pubsub
.. _gunicorn: http://gunicorn.org/
.. _gevent: http://www.gevent.org/
.. _server-sent events: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
