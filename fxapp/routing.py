from django.urls import re_path, path
from .consumers import FxConsumer

websocket_urlpatterns = [
    re_path(r'ws/api/fx/update/$', FxConsumer.as_asgi()),
]