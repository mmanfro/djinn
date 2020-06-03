import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync

class ChatConsumer(AsyncWebsocketConsumer):
    def connect(self):
        self.token = self.scope['url_route']['kwargs']['token']
        self.room_group_name = 'chat_%s' % self.token
  
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        displayname = text_data_json['displayname']
        messagehtml = render_to_string('chat/message/incoming.html', {'message': message,
                                                                      'displayname': displayname})

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': messagehtml,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        displayname = event['displayname']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'displayname': displayname,
        }))