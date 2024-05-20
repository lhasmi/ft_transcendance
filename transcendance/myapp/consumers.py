# handle WebSocket connections
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

User = get_user_model()

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'online_status'
        self.room_group_name = f'status_{self.room_name}'#unique name for broadcast
        await self.channel_layer.group_add(# Joining the group to receive messages
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):# Leaving the group on disconnect
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data['username']
        online_status = data['online_status']
        # Broadcasting the status update to all connected clients
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'status_message',
                'username': username,
                'online_status': online_status
            }
        )
    async def status_message(self, event):
        username = event['username']
        online_status = event['online_status']

        await self.send(text_data=json.dumps({
            'username': username,
            'online_status': online_status
        }))

# class GameConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'game_{self.room_name}'

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         move = data['move']

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'game_message',
#                 'move': move
#             }
#         )
#     async def game_message(self, event):
#         move = event['move']

#         await self.send(text_data=json.dumps({
#             'move': move
#         }))
