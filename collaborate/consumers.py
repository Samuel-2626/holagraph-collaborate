# Python Module
import json

# third-party libraries
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from asgiref.sync import async_to_sync

# current app modules
from . models import Channel, MessagesInChannel

# django apps
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser


class ChannelConsumer(AsyncWebsocketConsumer):

  """
    This a chat server created for each channel to make communication happen in real-time 
  """
  
  async def connect(self):

    # Get the Channel id from the argument of routing.py

    self.channel_uuid = self.scope['url_route']['kwargs']['channel_uuid']


    # Get the Current Authenticated User from the Scope

    self.user = self.scope['user']


    # Make a database connection to get the channel name and object

    self.channel_group_name = await self.get_channel_name()


    self.channel_object = await self.get_channel()


    # Join channel group
    await self.channel_layer.group_add(
      self.channel_group_name,
      self.channel_name,
    )

    # accept connection
    await self.accept()

  
  @database_sync_to_async
  def get_channel_name(self):
    channel = Channel.objects.get(pk=self.channel_uuid)
    return channel.slug

  @database_sync_to_async
  def get_channel(self):
    channel = Channel.objects.get(pk=self.channel_uuid)
    return channel


  async def disconnect(self, close_code):
    # Leave channel group
    await self.channel_layer.group_discard(
      self.channel_group_name,
      self.channel_name,
    )

  # Receive message from websocket
  async def receive(self, text_data):
    text_data_json = json.loads(text_data)
    message = text_data_json['message']
    now = timezone.now()

    # Store Message In Database
    self.store_message_in_db = await self.store_message(message)


    # Send message from room group
    await self.channel_layer.group_send(
      self.channel_group_name,
      {
        'type': 'chat_message',
        'message': message,
        'user': self.user.username,
        'datetime': now.isoformat(),
      }
    )

  # receive message from room group
  async def chat_message(self, event):
    # send message to Websocket
    await self.send(text_data=json.dumps(event))

  
  # Function to store message to the database
  @database_sync_to_async
  def store_message(self, message):
    MessagesInChannel.objects.create(channel=self.channel_object, person=self.scope['user'], message=message)
