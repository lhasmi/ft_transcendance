import os
import django
import logging
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from myapp.middleware import TokenAuthMiddleware
from myapp.routing import websocket_urlpatterns

logging.basicConfig(level=logging.DEBUG)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcendance.settings')
django.setup()

logging.debug("Django setup completed.")

# Initialize Django ASGI application early to ensure the apps are loaded.
django_asgi_app = get_asgi_application()
logging.debug("ASGI application initialized.")


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": TokenAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
logging.debug("ProtocolTypeRouter configured.")
