# for WebSocket URLs
from django.urls import re_path
from myapp.consumers import StatusConsumer

websocket_urlpatterns = [
    re_path(r'^ws/status/$', StatusConsumer.as_asgi()),  # routes to a single status WebSocket connection
]
