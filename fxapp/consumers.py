# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class FxConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         print('Connected')
#         await self.accept()

#     async def disconnect(self, close_code):
#         print(f'Disconnecting:{close_code}')

#     async def send_update(self,event):
#         await self.send(text_data=json.dumps({'message': 'Database updated!'}))

#     async def receive(self, text_data=None):
#         print('receiving')
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         sender = text_data_json['sender']

#         print(message, sender)

#         #sending the message back to the client over the websocket connection
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'sender': sender
#         }), content_type="text/event-stream")

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class FxConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            print('Connected')
            await self.accept()
        except Exception as e:
            print(f"Error during connection: {str(e)}")

    async def disconnect(self, close_code):
        try:
            print(f'Disconnecting: {close_code}')
        except Exception as e:
            print(f"Error during disconnection: {str(e)}")

    async def send_update(self, event):
        try:
            await self.send(text_data=json.dumps({'message': 'Database updated!'}))
        except Exception as e:
            print(f"Error sending update: {str(e)}")

    async def receive(self, text_data=None, bytes_data=None):
        try:
            print('Receiving')
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            sender = text_data_json['sender']

            print(message, sender)

            # Sending the message back to the client over the websocket connection
            await self.send(text_data=json.dumps({
                'message': message,
                'sender': sender
            }), content_type="text/event-stream")
        except Exception as e:
            print(f"Error during message reception: {str(e)}")
