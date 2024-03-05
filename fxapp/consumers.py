
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


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)
   
class TradeConsumer(AsyncWebsocketConsumer):
    trade_update_group = "fx_tradeflow"
    TRADE_CHUNK_SIZE = 100  # Adjust chunk size based on data and network conditions

    async def connect(self):
        try:
            await self.accept()
            
            trades = await self.all_trades()
            await self.send_trade_list(trades)
            # await self.send(text_data=json.dumps({"initial_trade_list": trades}, cls=DecimalEncoder))
            await self.channel_layer.group_add(self.trade_update_group, self.channel_name)
            # 
            # 
        except Exception as e:
            print(f"Error in connect: {e}")
            traceback.print_exc() # Print the traceback

    async def send_initial_data(self):
        # Fetch the initial trade data
        trades = Trade.objects.all().order_by('-id')[:self.TRADE_CHUNK_SIZE]
        trade_data = TradeSerializer(trades, many=True).data

        # Send the initial chunk
        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            'data': trade_data
        }))

        # Schedule remaining chunks (if any)
        remaining_trades = trades.count() - self.TRADE_CHUNK_SIZE
        if remaining_trades > 0:
            for i in range(0, remaining_trades, self.TRADE_CHUNK_SIZE):
                await asyncio.sleep(0.1)  # Add a slight delay between chunks
                next_chunk = trades[i + self.TRADE_CHUNK_SIZE: i + 2 * self.TRADE_CHUNK_SIZE]
                next_chunk_data = TradeSerializer(next_chunk, many=True).data
                await self.send(text_data=json.dumps({
                    'type': 'data_chunk',
                    'data': next_chunk_data
                }))
                
# .order_by('last_updated')[:self.TRADE_CHUNK_SIZE]
                
    @database_sync_to_async
    def all_trades(self):
        trades = Trade.objects.all()
        trade_serializer = TradeSerializer(trades, many=True)
        trades_data = trade_serializer.data
        return trades_data
    

    async def trade_updated(self, trade_data):
        trades = await self.all_trades()
        await self.send_trade_list(trades)
        # await self.send(text_data=json.dumps({
        #         'trade_updated':trade_data
        #     }, cls=DecimalEncoder))
        

    async def send_trade_list(self, trades):
        try:
            trade_data = []
            for trade in trades:
                trade_data.append(trade)
            await self.send(text_data=json.dumps({
                'type':'trade_list',
                'data':trade_data
            }, cls=DecimalEncoder))
        except Exception as e:
            print(f"Error sending trade list: {e}")
            print(traceback.format_exc())  # Print the traceback

    @database_sync_to_async
    def broadcast_trade_update(self, trade_data):
        """Send trade update to the group."""
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            self.trade_update_group, {"type": "trade_updated", "data": trade_data}
        )

    async def disconnect(self, close_code):
        # await self.channel_layer.group_discard(self.trade_update_group, self.channel_name)
        self.close(close_code)

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
                trade_data = serializer.data  # Use serializer.data for efficient serialization
                # trade_data = self.all_trades() # Use serializer.data for efficient serialization
                async_to_sync(self.broadcast_trade_update)(trade_data)
                # async_to_sync(self.broadcast_trade_list)
            else:
                print( serializer.errors)
        except Exception as e:
            print(f"Error saving trade to database: {e}")
            traceback.print_exc()  # Print the traceback

# Connect consumer to Trade signals
@receiver(post_save, sender=Trade)
async def trade_updated_signal(sender, instance, created, **kwargs):
        print('instanxe ', instance)
        print('sender ', sender, created)
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            "fx_tradeflow", {"type": "trade_updated", "data": instance}
        )

@receiver(post_delete, sender=Trade)
async def trade_deleted_signal(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    # trades = await TradeConsumer().all_trades()  # Fetch the entire trade list
    # await channel_layer.group_send(
        # "fx_tradeflow", {"type": "trade_list", "data": trades})
    await channel_layer.group_send(
        "fx_tradeflow", {"type": "trade_deleted", "data": instance.pk}
    )


        
