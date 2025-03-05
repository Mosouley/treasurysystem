import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "treasurysystem.settings")


from celery.schedules import crontab  


app = Celery("treasurysystem")
app.config_from_object("django.conf:settings", namespace="CELERY")

# app.conf.beat_schedule = {  
#     'send-position-updates-every-5-minutes': {  
#         'task': 'treasurysystem.tasks.send_position_updates',  
#         'schedule': crontab(minute='*/5'),  # Every 5 minutes  
#     },  
# }  

# app.conf.beat_schedule = {
#     'update-exchange-rates-every-5-minutes': {
#         'task': 'fxapp.tasks.update_exchange_rates_task',
#         'schedule': crontab(minute='*/5'),
#     },
# }
app.autodiscover_tasks()