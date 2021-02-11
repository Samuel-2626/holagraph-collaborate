from django.urls import path

from . import consumers

websockets_urlpatterns = [
  path('ws/chat/channel/<channel_uuid>/', consumers.ChannelConsumer),
]