
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Trade
from .serializers import TradeSerializer
from channels.db import database_sync_to_async
import traceback
import decimal
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import date
from treasurysystem.utils import get_positions, broadcast_data

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)
   
class TradeConsumer(AsyncWebsocketConsumer):
    trade_update_group = "fx_tradeflow"

    async def connect(self):
        try:
            await self.accept()
            # trades = await self.all_trades_day()
            await self.send_trade_list()
            await self.channel_layer.group_add(self.trade_update_group, self.channel_name)
            # 
            # 
        except Exception as e:
            print(f"Error in connect: {e}")
            traceback.print_exc() # Print the traceback
    
    @database_sync_to_async
    def all_trades_day(self):
        trades = Trade.objects.filter(date_created__gte=date.today()).order_by('-date_created')
        trade_serializer = TradeSerializer(trades, many=True)
        trades_data = trade_serializer.data
        return trades_data
  
    async def trade_updated(self, trade_data):
        trades = await self.all_trades()
        await self.send_trade_list(trades)
        # await self.send(text_data=json.dumps({
        #         'trade_updated':trade_data
        #     }, cls=DecimalEncoder))
        

    async def send_trade_list(self):

        trades = await self.all_trades_day()
        trade_data = []
        try: 
            for trade in trades:
                trade_data.append(trade)
            await self.send(text_data=json.dumps({
                'type':'trade_list',
                'data':trade_data
            }, cls=DecimalEncoder))
        except Exception as e:
            # print(f"Error sending trade list: {e}")
            print(traceback.format_exc())  # Print the traceback

    async def send_trades_of_day(self, event):
        # Fetch the trades data of the day
        trades = await self.all_trades_day()
        await self.send(text_data=json.dumps({
            'type': 'all_trades_day',
            'data': trades
        }, cls=DecimalEncoder))
    
    async def send_new_trades(self, event):
        # Fetch the new trades data
        new_trades = event['data']
        await self.send(text_data=json.dumps({
            'type': 'new_trades',
            'data': new_trades
        }, cls=DecimalEncoder))
    

    async def receive(self, text_data=None):
        data =  json.loads(text_data)
        trade_data = data.get('data', {})
        if isinstance(trade_data, str):
            trade_data = json.loads(trade_data)
        await self.save_trade_to_database(trade_data)

    @database_sync_to_async
    def save_trade_to_database(self, data):
        try:
            serializer = TradeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                print( serializer.errors)
        except Exception as e:
            print(f"Error saving trade to database: {e}")
            traceback.print_exc()  # Print the traceback

    @receiver(post_save, sender=Trade)
    def broadcast_trades(sender, instance, created, **kwargs):
        if created:
            channel_layer = get_channel_layer()
            trade_serializer = TradeSerializer(instance)
            trades_data = trade_serializer.data
            async_to_sync(channel_layer.group_send)(
                "fx_tradeflow", 
                {"type": "send_new_trades", 
                "data": trades_data,
                }
            )

            # update position as well
            data = get_positions()
           
            broadcast_data('position_updates','send_position_updates',data)



    async def disconnect(self, close_code):
        self.close(close_code)


class PositionConsumer(AsyncWebsocketConsumer):  
    async def connect(self):  
        await self.channel_layer.group_add("position_updates", self.channel_name)  
        await self.accept()  


    async def send_position_updates(self, event): 
        message = event['data']  
        # await self.send(text_data=json.dumps(message))  
        await self.send(text_data=json.dumps({
            'type': 'position_updates',
            'data': message
        }, cls=DecimalEncoder))      

    async def disconnect(self, close_code):  
        await self.channel_layer.group_discard("position_updates", self.channel_name)  
        
      