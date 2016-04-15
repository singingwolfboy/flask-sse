Advanced Usage
==============

Channels
--------
Sometimes, you may not want all events to be published to all clients.
For example, a client that cares about receiving the latest updates in their
social network probably doesn't care about receiving the latest statistics about
how many users are online across the entire site, and vice versa. When
publishing an event, you can select which channel to direct the event to.
If you do, only clients that are checking that particular channel will receive
the event. For example, this event will be sent to the "users.social"
channel:

.. code-block:: python

    sse.publish({"user": "alice", "status": "Life is good!"}, channel="users.social")

And this event will be sent to the "analytics" channel:

.. code-block:: python

    sse.publish({"active_users": 100}, channel="analytics")

Channel names can be any string you want, and are created dynamically as soon
as they are referenced. The default channel name that Flask-SSE uses is "sse".
For more information, `see the documentation for the
Redis pubsub system <http://redis.io/topics/pubsub>`_.

To subscribe to a channel, the client only needs to provide a ``channel``
query parameter when connecting to the event stream.
For example, if your event stream is at ``/stream``, you can connect to the
"users.social" channel by using the URL ``/stream?channel=users.social``.
You can also use Flask's :func:`~flask.url_for` function to generate this
query parameter, like so:

.. code-block:: python

    url_for("sse.stream", channel="users.social")

By default, all channels are publicly accessible to all users. However, see
the next section to change that.

Access Control
--------------
Since Flask-SSE is implemented as a :ref:`blueprint <flask:blueprints>`,
you can attach a :meth:`~flask.Blueprint.before_request` handler to implement
access control. For example:

.. code-block:: python

    @sse.before_request
    def check_access():
        if request.args.get("channel") == "analytics" and not g.user.is_admin():
            abort(403)
