"""
ASGI config for holagraph_collaborative_module project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import collaborate.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'holagraph_collaborative_module.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AllowedHostsOriginValidator(
    AuthMiddlewareStack(
      URLRouter(
        collaborate.routing.websockets_urlpatterns
      )
    ),
  ),
})
