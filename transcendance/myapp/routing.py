#  for WebSocket URLs
from django.urls import re_path
from myapp.consumers import StatusConsumer

websocket_urlpatterns = [
    re_path(r'^ws/status/$', StatusConsumer.as_asgi()), #routes to a single status WebSocket connection
]
	# re_path(r'ws/game/(?P<room_name>[\w-]+)/$', GameConsumer.as_asgi()), #enable unique room-based connections for games and chats
