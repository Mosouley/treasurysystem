# signals.py
from django.db.models import Sum, Count, Avg, Max, Min, Q
from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Trade, Position,  Ccy
from decimal import Decimal
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Trade)
def update_position_on_save(sender, instance, **kwargs):
    date = instance.tx_date
    ccy1 = instance.ccy1
    ccy2 = instance.ccy2
    amount1 = instance.amount1 if instance.buy_sell == 'buy' else -instance.amount1
    amount2 = instance.amount2 if instance.buy_sell == 'sell' else -instance.amount2


    #Function to update position
    def update_position(date, ccy, amount):

        try:
            with transaction.atomic():
                position, created = Position.objects.get_or_create(date=date, ccy=ccy,defaults={'intraday_pos': 0})
                position.intraday_pos += amount
                position.save()

        except Exception as e:
                logger.error(f"Error updating the position: {e}")

    # Update or create position for ccy1
    update_position(date, ccy1, amount1)

    # Update or create position for ccy2
    update_position(date, ccy2, amount2)

    # Ensure all currencies in the system have a position entry
    for cur in Ccy.objects.all():
        if cur != ccy1 and cur != ccy2:
            update_position(date, cur, 0)
   

@receiver(post_delete, sender=Trade)
def update_position_on_delete(sender, instance, **kwargs):
    date = instance.tx_date
    ccy = instance.ccy1
    amount = instance.amount1 if instance.buy_sell == 'buy' else -instance.amount1
    try:
        with transaction.atomic():
            position = Position.objects.get(date=date, ccy=ccy)
            position.intraday_pos -= amount
            position.save()
    except Position.DoesNotExist:
        logger.warning(f"Position does not exist for date {date} and currency {ccy}.")
    except Exception as e:
        logger.error(f"Error updating position on delete: {e}")