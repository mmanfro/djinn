import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string


class ChatConsumer(WebsocketConsumer):
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
        message_incoming = render_to_string('chat/message/incoming.html', {'message': message,
                                                                      'displayname': displayname})
        message_outgoing = render_to_string('chat/message/outgoing.html', {'message': message,
                                                                      'displayname': displayname})

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_incoming': message_incoming,
                'message_outgoing': message_outgoing,
                'displayname': displayname
            }
        )

    # Receive message from room group
    def chat_message(self, event):
#         message = event['message']
        message_incoming = event['message_incoming']
        message_outgoing = event['message_outgoing']
        displayname = event['displayname']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
#             'message': message,
            'message_incoming': message_incoming,
            'message_outgoing': message_outgoing,
            'displayname': displayname,
        }))