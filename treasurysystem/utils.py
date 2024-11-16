import random
import string
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits ):
    return ''.join(random.choice(chars) for _ in range(size))

# print(random_string_generator())
# print('---vvv^^^^----')
# print(random_string_generator(size=50))
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
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': event_type,
                'data': data
            }
        )
    else:
        print("Error: Channel layer not found.")