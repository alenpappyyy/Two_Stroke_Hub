"""
ASGI config for two_stroke_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import notifications.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "two_stroke_backend.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            notifications.routing.websocket_urlpatterns
        )
    ),
})


from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def notify(user, message):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",
            "message": message
        }
    )


import dashboard.routing

URLRouter(
    notifications.routing.websocket_urlpatterns +
    dashboard.routing.websocket_urlpatterns
)
