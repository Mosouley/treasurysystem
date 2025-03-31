from celery import shared_task

from django.core.management import call_command

@shared_task
def send_email_report():
    call_command("email_report_day", )


@shared_task  
def send_position_updates():  
    call_command('send_positions') 


@shared_task
def update_rates_task():
    call_command('update_exchange_rates')