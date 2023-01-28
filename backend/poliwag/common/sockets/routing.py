from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter

from .notifications import consumers
from .authentication import SimpleJWTAuthMiddlewareStack


websocket_urlpatterns = [
    re_path(r"ws/", consumers.NotificationConsumer),
]


application = ProtocolTypeRouter(
    {
        "websocket": SimpleJWTAuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
