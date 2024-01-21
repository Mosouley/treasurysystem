import json
from channels.generic.websocket import AsyncWebsocketConsumer

class FxConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('Connected')
        await self.accept()

    async def disconnect(self, close_code):
        print(f'Disconnecting:{close_code}')

    async def send_update(self,event):
        await self.send(text_data=json.dumps({'message': 'Database updated!'}))

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']

        print(message, sender)

        #sending the message back to the client over the websocket connection
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))