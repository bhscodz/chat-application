import json
from . import models
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user=self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        if self.user.is_authenticated:
            self.room_group_name = 'chat_%s' % self.room_name

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        else:
            self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username=self.user.username
        await self.save_message_to_db(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))
    @sync_to_async
    def save_message_to_db(self,message):
        room_obj=get_object_or_404(models.chatrooms,name=self.room_name)
        msg_obj=models.messages(
            author=self.user,
            text=message,
            chatroom=room_obj
        )
        msg_obj.save()
    pass