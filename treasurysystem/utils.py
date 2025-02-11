import random
import string
import traceback
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from channels.db import database_sync_to_async
from django.utils.text import slugify
from django.db.models import OuterRef, Subquery
from asgiref.sync import sync_to_async
from decimal import Decimal

from fxapp.models import Position
from fxapp.serializers import PositionSerializer

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits ):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_order_id_generator(instance):
    order_new_id = random_string_generator() #can put upper here
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return order_new_id

def unique_slug_generator(instance, new_slug=None):
    '''
    This assumes you have a slug field and a title field
    '''
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f'{slug}{random_string_generator(size=4)}'
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def broadcast_data(group_name, event_type, data):
    """
    Sends data to a specified WebSocket channel group.
    
    Args:
        group_name (str): The name of the channel group.
        event_type (str): The type of event to send (matches consumer method).
        data (dict): The data payload to broadcast.
    """
    channel_layer = get_channel_layer()
    # print(f"Broadcasting to {group_name}, data: {data}")  # 

    if channel_layer:
        try:
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': event_type,
                    'data': data
                }
            )
            # print(f"Successfully broadcast to {group_name}")  # Debug log
        except Exception as e:
            print(f"Error broadcasting to {group_name}: {e}")
            traceback.print_exc()
    else:
        print("Error: Channel layer not found.")

# @database_sync_to_async
@sync_to_async
def get_positions():
    """
    Fetch the latest open position for each currency, regardless of the date.
    """
    latest_date_subquery = Position.objects.filter(
        ccy=OuterRef('ccy')
    ).order_by('-date').values('date')[:1]

    queryset = Position.objects.filter(date=Subquery(latest_date_subquery))
    serializer = PositionSerializer(queryset, many=True)
    data = serializer.data
   
    return data


def get_pivot():
    from django.db.models import F
    from fxapp.models import SystemDailyRates
    # Query all rates
    rates = SystemDailyRates.objects.all()

    # Transform rates into a pivot table structure
    from collections import defaultdict

    pivot_table = defaultdict(dict)  # {ccy_code: {date: rate}}

    for rate in rates:
        pivot_table[rate.ccy.code][rate.date] = rate.exchange_rate

    # Convert to a simple table-like format for display
    table = []
    dates = sorted({rate.date for rate in rates})  # Sorted unique dates

    for ccy_code, rates in pivot_table.items():
        row = {'Currency': ccy_code}
        for date in dates:
            row[str(date)] = rates.get(date, None)  # Fill missing rates with None
        table.append(row)

def calculate_interest(principal_amount, interest_rate, start_date, maturity_date, days_convention):
    """
    Calculate interest based on the days convention, value date, and maturity date.

    Args:
        principal_amount (Decimal): The principal amount.
        interest_rate (Decimal): The interest rate.
        start_date (date): The start date of the deal.
        maturity_date (date): The maturity date of the deal.
        days_convention (str): The days convention (e.g., 'ACT/360', 'ACT/365', '30/360').

    Returns:
        Decimal: The calculated interest.
    """
    days = (maturity_date - start_date).days
    if days_convention == 'ACT/360':
        interest = (principal_amount * interest_rate * days) / 360
    elif days_convention == 'ACT/365':
        interest = (principal_amount * interest_rate * days) / 365
    elif days_convention == '30/360':
        interest = (principal_amount * interest_rate * 30 * (days // 30)) / 360
    else:
        interest = Decimal('0.00')
    return interest