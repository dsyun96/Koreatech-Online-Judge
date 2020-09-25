from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from .infos import results_ko
from .models import Submit
from .tasks import run


class IdeConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        payload = json.loads(text_data)
        run.delay(self.channel_name, payload['code'], payload['lang'], payload['input'])

    def task_result(self, event):
        self.send(text_data=json.dumps(event))


class StatusConsumer(WebsocketConsumer):
    def connect(self):
        print('connect')
        self.accept()

    def disconnect(self, code):
        for submit_id in self.submit_ids:
            async_to_sync(self.channel_layer.group_discard)(
                submit_id,
                self.channel_name
            )

    def receive(self, text_data):
        print('receive')
        payload = json.loads(text_data)
        self.submit_ids = [str(i) for i in payload['submit_ids']]

        for submit_id in self.submit_ids:
            submit = Submit.objects.get(pk=submit_id)
            if submit.result in [None, Submit.SubmitResult.ING]:
                async_to_sync(self.channel_layer.group_add)(
                    submit_id,
                    self.channel_name
                )
            else:
                self.send(text_data=json.dumps({
                    'result': f'{results_ko[submit.result]}',
                    'id': submit.id,
                    'memory': submit.memory,
                    'runtime': submit.runtime,
                }))

    def task_result(self, event):
        print('A' * 50)
        print(event)
        self.send(text_data=json.dumps(event))
