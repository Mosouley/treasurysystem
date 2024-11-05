from django.urls import path, re_path
from .consumers import TradeConsumer,PositionConsumer


websocket_urlpatterns = [
    path('ws/api/fx/trade_update/', TradeConsumer.as_asgi()),
    re_path(r'ws/api/fx/positions/$', PositionConsumer.as_asgi()),
]