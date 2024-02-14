
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Trade
from .serializers import TradeSerializer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async ,async_to_sync
from django.core.serializers import serialize
import traceback
import decimal

class TradeConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def all_trades(self):
        trades = Trade.objects.all()
        
        trade_serializer = TradeSerializer(trades, many=True)
        trades_data = trade_serializer.data
        return trades_data
    
    async def send_trade_list(self, trades):
        try:
            await self.send(text_data=json.dumps({
                'trade_list':trades
            }, cls=DecimalEncoder))
        except Exception as e:
            print(f"Error sending trade list: {e}")
            print(traceback.format_exc())  # Print the traceback
        
    
    async def connect(self):
        try:
            await self.accept()
        
            trades = await self.all_trades()
            await self.send_trade_list(trades)
        except Exception as e:
            print(f"Error in connect: {e}")
            print(traceback.format_exc())  # Print the traceback

            # Add the connected client to a group named 'fx_updates'
            # await self.channel_layer.group_add('fx_tradeflow', self.channel_name)
    

    async def disconnect(self, close_code):
        # await self.channel_layer.group_discard('fx_tradeflow', self.channel_name)
        self.close(close_code)

    async def receive(self, text_data=None):
        data =  json.loads(text_data)
        trade_data = data.get('data', {})
        print(trade_data)
          # Extract trade data and save to the database asynchronously
        await self.save_trade_to_database(trade_data)
        # no needtosendthe trade data for now
        # json_data = json.dumps(trade_data )
        # print(json_data)
        # await self.send_trade_update(data)

    @database_sync_to_async
    def save_trade_to_database(self, data):
        trade_data = data.get('trade', {}).get('data', {})
        print(trade_data)
        serializer = TradeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

    async def send_trade_update(self, event):
        await self.send(text_data=json.dumps({
            'trade': event
        }))
     


    async def update_trade_data(self, event):
        data = event['data']
        await self.send_trade_data(data)   
    #     await self.channel_layer.group_send(
    #         self.groupname,
    #         {
    #             'type': 'deprocessing',
    #             'value': val
    #         }
    #     )
        
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)
   