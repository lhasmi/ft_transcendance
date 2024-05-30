import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]  # Extract user from scope
        if self.user.is_authenticated:
            await self.set_online_status()
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.set_offline_status()

    async def receive(self, text_data):  # Handle incoming messages (if needed)
        data = json.loads(text_data)
        username = data.get('username')
        online_status = data.get('online_status')
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

    @database_sync_to_async
    def set_online_status(self):
        self.user.player.set_online()

    @database_sync_to_async
    def set_offline_status(self):
        user = User.objects.get(id=self.user.id)
        user.player.set_offline()
