from django.core.management.base import BaseCommand  
from treasurysystem.utils import broadcast_data, get_positions


class Command(BaseCommand):  
    help = 'Send position summaries over WebSocket' 

    def handle(self, *args, **options):
        data = get_positions()
        broadcast_data('position_updates','send_position_updates',data)
 