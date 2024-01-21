"""
ASGI config for treasurysystem project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.middleware import BaseMiddleware
from django.core.asgi import get_asgi_application
from fxapp import routing

class CorsMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        if "websocket.connect" in scope["type"]:
            # You can customize the allowed origins based on your needs
            headers = [
                (b"access-control-allow-origin", b"http://localhost:4200"),
                # Add other CORS headers if needed
            ]
            for header, value in headers:
                scope["headers"].append((header, value))
        return await super().__call__(scope, receive, send)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'treasurysystem.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter  (
    {
    'http': django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)),
    ),
})



