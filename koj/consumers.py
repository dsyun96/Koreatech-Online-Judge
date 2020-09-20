from channels.generic.websocket import WebsocketConsumer
import json
from .runs import *


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        run_func = [run_c, ]

        with open('test_input', 'w') as f:
            f.write(text_data_json['input'])

        result = run_func[int(text_data_json['lang'])](text_data_json['code'], text_data_json['input'])

        # task = run.delay(text_data_json['code'], text_data_json['lang'], text_data_json['input'])
        # result = task.wait(timeout=None, interval=1)

        self.send(text_data=json.dumps({
            'message': result
        }))

        '''self.send(text_data=json.dumps({
            'message': message
        }))'''
