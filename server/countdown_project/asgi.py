import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import timer.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "countdown_project.settings")
django.setup()

# Debugging WebSocket connections
async def websocket_application(scope, receive, send):
    print(f"🔹 WebSocket connection received: {scope['path']}")
    await send({"type": "websocket.close"})  # Closes connection immediately for debugging

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(timer.routing.websocket_urlpatterns)
    ),
})
