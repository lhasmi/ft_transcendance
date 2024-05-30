"""
ASGI config for transcendance project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import logging

logging.basicConfig(level=logging.DEBUG)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcendance.settings')
django.setup()

logging.debug("Django setup completed.")

# Initialize Django ASGI application early to ensure the apps are loaded.
django_asgi_app = get_asgi_application()
logging.debug("ASGI application initialized.")

from myapp.middleware import TokenAuthMiddleware
from myapp.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": TokenAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})
logging.debug("ProtocolTypeRouter configured.")


# import os
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# from myapp.routing import websocket_urlpatterns
# from myapp.middleware import TokenAuthMiddleware
# from channels.auth import AuthMiddlewareStack 

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcendance.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": TokenAuthMiddleware(
#             URLRouter(
#                 websocket_urlpatterns
#             )
#     ),
# })

