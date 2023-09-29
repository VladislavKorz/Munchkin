import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from room import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sites.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter([
        path("ws/race/", consumers.RaceSyncConsumer.as_asgi()),
        path("ws/class/", consumers.ClassSyncConsumer.as_asgi()),
        path("ws/level/", consumers.LevelSyncConsumer.as_asgi()),
        path("ws/power/", consumers.PowerSyncConsumer.as_asgi()),
        path("ws/gender/", consumers.GenderSyncConsumer.as_asgi()),
        path("ws/request_connection/", consumers.ConnectionRequestSyncConsumer.as_asgi()),
    ]),
})
