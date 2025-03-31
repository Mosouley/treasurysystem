from django.core.management.base import BaseCommand, CommandError
from fxapp.models import Position
from datetime import timedelta, datetime
from django.db.models import Sum
from django.utils import timezone
from django.utils.timezone import make_aware


today = timezone.now() - timedelta(60)

class Command(BaseCommand):
    help = "A description of the command"

    # def handle(self, *args, **options):
    #     self.stdout.write("Running My position EOD")
    #     queryset = Position.objects.all().values('date','ccy__code').annotate(total_pos=Sum('intraday_pos')).filter(date=today)
    
    #     serializer = PositionSummarySerializer(queryset, many=True)  
    #     data = serializer.data 
    #     self.stdout.write(data)