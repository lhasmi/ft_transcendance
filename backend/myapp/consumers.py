# handle WebSocket connections
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async 

User = get_user_model()

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"] # Extract user from scope
        # If the user is authenticated, set them online and accept the connection
        if self.user.is_authenticated:
            await self.set_online_status()
            await self.accept()
        else:# Close the connection if the user is not authenticated
            await self.close()
        # self.room_name = 'online_status'
        # self.room_group_name = f'status_{self.room_name}'#unique name for broadcast
        # await self.channel_layer.group_add(# Joining the group to receive messages
        #     self.room_group_name,
        #     self.channel_name
        # )
        # await self.accept()
    async def disconnect(self, close_code):
        # If the user is authenticated, set them offline when they disconnect
        if self.user.is_authenticated:
            await self.set_offline_status()
        # await self.channel_layer.group_discard(
        #     self.room_group_name,
        #     self.channel_name
        # )
    async def receive(self, text_data):# Handle incoming messages (if needed)
        data = json.loads(text_data)
        username = data.get('username')
        online_status = data.get('online_status')
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

    @database_sync_to_async
    def set_online_status(self):
        # Increment the user's online status count
        self.user.player.set_online()

    @database_sync_to_async
    def set_offline_status(self):
        # Decrement the user's online status count
        self.user = User.objects.get(id=self.user.id)
        self.user.player.set_offline()