import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import *

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name='chat_%s'% self.room_name
        self.user=self.scope['user']
        print(self.user)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'tester_message',
                'tester':'hello there'

            }
        )
    async def recive(self,text_data):
        print(text_data)
        await self.send(text_data='hello')
        await self.close()
    async def disconnect(self, code):
        pass