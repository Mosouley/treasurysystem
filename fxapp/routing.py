from django.urls import re_path, path
from .consumers import FxConsumer

websocket_urlpatterns = [
    path('ws/update/', FxConsumer.as_asgi()),
]