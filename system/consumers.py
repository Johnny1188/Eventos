import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from channels.db import database_sync_to_async
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        def getMessages(self):
            messages = Message.objects.filter(chatName=self.room_group_name).order_by('-id')[:20].values('text','sender')
            messagesToReturn = []
            for message in messages:
                messagesToReturn.insert(0,{'sender':message['sender'],'text':message['text']})
            return messagesToReturn
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.last_messages = await database_sync_to_async(getMessages)(self)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Admits the user to connect - If authorization is needed -> put some logic and then decide reject/accept
        await self.accept()

        for message in self.last_messages:
            await self.send(text_data=json.dumps({
            'text': message['text'],
            'sender': message['sender'],
            'isPastMessage': True
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['text']
        sender = text_data_json['sender']
        def saveMessage(self):
            user = User.objects.get(pk=sender)
            newMsg = Message.objects.create(text=message,sender=user,chatName=self.room_group_name)
            newMsg.save()
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': message,
                'sender': sender
            }
        )
        # Save the message into database:
        await database_sync_to_async(saveMessage)(self)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['text']
        sender = event['sender']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'text': message,
            'sender': sender
        }))