# server/timer/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"^ws/timer/(?P<event_id>\d+)/$", consumers.TimerConsumer.as_asgi()),
]
