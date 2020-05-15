from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from chat.models import CustomUser, Chat, Message, MessageContent


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    # Обработка сообщения пользователя из бразуера
    async def receive(self, text_data):
        json_data = json.loads(text_data)
        message = json_data['message']
        username = json_data['username']

        # user = await database_sync_to_async(CustomUser.objects.get)(username=username)
        # chat = await database_sync_to_async(Chat.objects.get)(id=self.room_name)
        # message_content = await database_sync_to_async(MessageContent.objects.create)(text=message)
        # message_object = await database_sync_to_async(Message.objects.create)(chat=chat,
        #                                                                       author=user,
        #                                                                       content=message_content)
        #
        # time = message_object.time.strftime('%I:%M')
        time = ""

        # Send message to room group
        # Что отправить другим пользователям чата
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'time': time

            }
        )

    # Receive message from room group
    # Получение сообщения от других пользователей
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        time = event['time']
        # Send message to WebSocket
        # Что отправить пользователю
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'time': time
        }))
