from channels.generic.websocket import WebsocketConsumer
import json

from .tasks import run


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        payload = json.loads(text_data)

        with open('test_input', 'w') as f:
            f.write(payload['input'])
        run.delay(self.channel_name, payload['code'], payload['lang'], payload['input'])

    def task_result(self, event):
        self.send(text_data=json.dumps({
            'message': event['message']
        }))