import os
import django
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("!!!!!! !!!!!! Setting DJANGO_SETTINGS_MODULE environment variable!!!!!! !!!!!! ")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcendance.settings')

logger.debug("Calling django.setup()")
try:
    django.setup()
    logger.debug("!!!!!! !!!!!! Django setup completed successfully !!!!!! !!!!!! ")
except Exception as e:
    logger.error(f"Django setup failed: {e}")
    raise


from django.core.asgi import get_asgi_application

# Initialize the ASGI application
try:
    django_asgi_app = get_asgi_application()
    logger.debug("!!!!!! ASGI application loaded successfully!!!!!! ")
except Exception as e:
    logger.error(f"!!!!!! Failed to load ASGI application !!!!!! : {e}")
    raise

from channels.routing import ProtocolTypeRouter, URLRouter
from myapp.middleware import TokenAuthMiddlewareStack
from myapp.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": TokenAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

logger.debug("!!!!!! ASGI application initialized !!!!!! ")
logger.debug("!!!!!! ProtocolTypeRouter configured !!!!!! ")

# django.setup()

# print("!!!!!! Django setup completed. !!!!!!")


# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": TokenAuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })
# print("!!!!!! ASGI application initialized. !!!!!!")
# print("!!!!!! ProtocolTypeRouter configured. !!!!!!")
