
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Trade
from .serializers import TradeSerializer
from channels.db import database_sync_to_async
import traceback
import decimal
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from datetime import date

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
            print(f"Error sending trade list: {e}")
            print(traceback.format_exc())  # Print the traceback

    # @database_sync_to_async
    # def broadcast_trade_update(self, trade_data):
    #     """Send trade update to the group."""
    #     channel_layer = get_channel_layer()
    #     async_to_sync(channel_layer.group_send)(
    #         self.trade_update_group, {"type": "send_trade_list", "data": trade_data}
    #     )
    async def send_trades_of_day(self, event):
        # Fetch the trades data of the day
        trades = await self.all_trades_day()
        await self.send(text_data=json.dumps({
            'type': 'all_trades_day',
            'data': trades
        }, cls=DecimalEncoder))
    

    async def receive(self, text_data=None):
        data =  json.loads(text_data)
        trade_data = data.get('data', {})
        if isinstance(trade_data, str):
            trade_data = json.loads(trade_data)
        await self.save_trade_to_database(trade_data)

    @database_sync_to_async
    def save_trade_to_database(self, data):
        # print(data)
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
            trades = Trade.objects.filter(date_created__gte=date.today()).order_by('-date_created')
        
            trade_serializer = TradeSerializer(trades, many=True)
            trades_data = trade_serializer.data
            async_to_sync(channel_layer.group_send)(
                "fx_tradeflow", 
                {"type": "send_trades_of_day", 
                "data": trades_data,
                }
            )

        async def disconnect(self, close_code):
            # await self.channel_layer.group_discard(self.trade_update_group, self.channel_name)
            self.close(close_code)


                
      