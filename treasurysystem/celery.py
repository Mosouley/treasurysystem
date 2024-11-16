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
app.autodiscover_tasks()