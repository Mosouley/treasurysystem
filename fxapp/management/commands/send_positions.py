from django.core.management.base import BaseCommand  
from django.db.models import Sum
from fxapp.models import Position
from fxapp.views  import PositionSerializer
from channels.layers import get_channel_layer  
from asgiref.sync import async_to_sync  
from datetime import timedelta
from django.utils import timezone
from treasurysystem.utils import broadcast_data


class Command(BaseCommand):  
    help = 'Send position summaries over WebSocket' 

    def get_positions(self):
        today = timezone.now().date()
        # self.stdout.write(f"Today: {today}")
        queryset = Position.objects.values('date', 'ccy__code').annotate(total_pos=Sum('intraday_pos')).filter(date=today)
        # self.stdout.write(f"Queryset result **** >>>: {queryset}")

        serializer = PositionSerializer(queryset, many=True)  
        data = serializer.data

        return data

    def handle(self, *args, **options):
        
        today = timezone.now().date()
        # self.stdout.write(f"Today: {today}")
        queryset = Position.objects.values('date', 'ccy__code').annotate(total_pos=Sum('intraday_pos')).filter(date=today)
        # self.stdout.write(f"Queryset result **** >>>: {queryset}")

        serializer = PositionSerializer(queryset, many=True)  
        data = serializer.data 

        my_data = self.get_positions()
        self.stdout.write("sending my data ", my_data)


        broadcast_data('position_updates','send_position_updates',my_data)

        # channel_layer = get_channel_layer()
        # if channel_layer is None:
        #     self.stdout.write("Error: Channel layer not found.")
        #     return

        # async_to_sync(channel_layer.group_send)(
        #     'position_updates',
        #     {
        #         'type': 'send_position_updates',
        #         'data': data
        #     }
        # )

 