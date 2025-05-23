from datetime import timedelta, time, datetime

from django.core.mail import mail_admins
from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware
from fxapp.models import Trade, Position
from datetime import timedelta, datetime
from django.db.models import Sum


today = timezone.now() - timedelta(60)
tomorrow = today + timedelta(1)
today_start = make_aware(datetime.combine(today, time()))
today_end = make_aware(datetime.combine(tomorrow, time()))


class Command(BaseCommand):
    help = "Send Today's Trades Report to Admins"
    

    def handle(self, *args, **options):

        mon_query = Position.objects.all()

        trades = Trade.objects.filter(tx_date__gte=today_start)

        if trades:
            message = ""

            # for trade in trades:
                # message += f" { trade.buy_sell } - {trade.ccy1 } - {trade.ccy2 } - { trade.amount1 } - { trade.amount2 } \n"
            message += f" { mon_query}  \n"

            subject = (
                f"Trade Report for {today_start.strftime('%Y-%m-%d')} "
                f"to {today_end.strftime('%Y-%m-%d')}"
            )

            mail_admins(subject=subject, message=message, html_message=None)

            self.stdout.write("E-mail Report was sent.")
        else:
            self.stdout.write("No Trades confirmed today.")