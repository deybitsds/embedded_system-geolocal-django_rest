from django.urls import re_path
from geolocal import consumers

websocket_urlpatterns = [
    re_path(r'ws/location/$', consumers.LocationConsumer.as_asgi()),
]