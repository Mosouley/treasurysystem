from django.core.management.base import BaseCommand  
from treasurysystem.utils import broadcast_data, get_positions


class Command(BaseCommand):  
    help = 'Send position summaries over WebSocket' 

    # def get_positions(self):
    #     today = timezone.now().date()
    #     # self.stdout.write(f"Today: {today}")
    #     queryset = Position.objects.values('date', 'ccy__code').annotate(total_pos=Sum('intraday_pos')).filter(date=today)
    #     # self.stdout.write(f"Queryset result **** >>>: {queryset}")

    #     serializer = PositionSerializer(queryset, many=True)  
    #     data = serializer.data

    #     return data

    def handle(self, *args, **options):
        
        # today = timezone.now().date()
        # # self.stdout.write(f"Today: {today}")
        # queryset = Position.objects.values('date', 'ccy__code').annotate(total_pos=Sum('intraday_pos')).filter(date=today)
        # # self.stdout.write(f"Queryset result **** >>>: {queryset}")

        # serializer = PositionSerializer(queryset, many=True)  
        # data = serializer.data 

        data = get_positions()

        broadcast_data('position_updates','send_position_updates',data)

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

 