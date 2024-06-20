from django.urls import path
from .consumers import TradeConsumer


websocket_urlpatterns = [
    path('ws/api/fx/trade_update/', TradeConsumer.as_asgi()),
]