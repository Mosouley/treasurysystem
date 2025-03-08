from django.core.management.base import BaseCommand  
from treasurysystem.utils import broadcast_data, get_positions
from asgiref.sync import async_to_sync
from django.utils import timezone

class Command(BaseCommand):  
    help = 'Send position summaries over WebSocket' 

    def handle(self, *args, **options):

        # Convert async get_positions to sync
        # data = get_positions_sync()
        # if data is not None:
        # # If broadcast_data is async
        #     async_to_sync(broadcast_data)(
        #         'position_updates',
        #         'send_position_updates',
        #         data
        #     )
        # else:
        #     print('No data to send')
        data = get_positions()
        broadcast_data('position_updates','send_position_updates',data)
 