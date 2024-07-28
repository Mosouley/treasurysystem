from datetime import timedelta, time, datetime

from django.core.mail import mail_admins
from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware
from fxapp.models import Trade


today = timezone.now()
tomorrow = today + timedelta(30)
today_start = make_aware(datetime.combine(today, time()))
today_end = make_aware(datetime.combine(tomorrow, time()))


class Command(BaseCommand):
    help = "Send Today's Trades Report to Admins"

    def handle(self, *args, **options):
        trades = Trade.objects.filter(date_created__range=(today_start, today_end))

        if trades:
            message = ""

            for trade in trades:
                message += f"{trade} \n"

            subject = (
                f"Trade Report for {today_start.strftime('%Y-%m-%d')} "
                f"to {today_end.strftime('%Y-%m-%d')}"
            )

            mail_admins(subject=subject, message=message, html_message=None)

            self.stdout.write("E-mail Report was sent.")
        else:
            self.stdout.write("No Trades confirmed today.")