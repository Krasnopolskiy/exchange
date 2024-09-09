from django.urls import re_path

from backend.stream.consumers import StreamConsumer

websocket_urlpatterns = [
    re_path(r"stream/$", StreamConsumer.as_asgi()),
]
