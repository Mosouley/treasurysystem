from django.core.management.base import BaseCommand  
from django.db.models import Sum  
from your_app.models import Position  
from your_app.serializers import PositionSummarySerializer  
from channels.layers import get_channel_layer  
from asgiref.sync import async_to_sync  
import json  

class Command(BaseCommand):  
    help = 'Send position summaries over WebSocket'  

    def handle(self, *args, **options):  
        # Get the position data  
        queryset = Position.objects.values('date', 'ccy__code').annotate(total_pos=Sum('position'))  
        
        # Serialize the data  
        serializer = PositionSummarySerializer(queryset, many=True)  
        data = serializer.data  
        
        # Send data over WebSocket  
        channel_layer = get_channel_layer()  
        async_to_sync(channel_layer.group_send)(  
            'position_updates',  # Group name for WebSocket  
            {  
                'type': 'send_position_updates',  
                'message': data  
            }  
        )  