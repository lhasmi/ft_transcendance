"""
ASGI config for transcendance project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from myapp.routing import websocket_urlpatterns
from myapp.middleware import TokenAuthMiddleware
from channels.auth import AuthMiddlewareStack 
# from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcendance.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # "websocket": AllowedHostsOriginValidator( #restricts WebSocket connections to the ALLOWED_HOSTS configured in settings.py
    "websocket": TokenAuthMiddleware(
            URLRouter(
                websocket_urlpatterns
            )
    ),
})


# application = get_asgi_application()
