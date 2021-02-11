# Python Modules
import uuid

# third-party libraries
from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField


# django apps
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.safestring import SafeString




""" Collaborative Application Model for Holograph """

class Room(models.Model):

  """ A model for creating a new room  """

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=255)
  description = models.CharField(max_length=255)
  slug = AutoSlugField(populate_from='title')
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_created_rooms')
  created_at = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ('title',)
    unique_together = [['title', 'created_by']]

  def __str__(self):
    return self.title


class People(models.Model):

  """ A model for adding people to room """

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='people')
  person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zz')
  joined = models.DateTimeField(auto_now_add=True)
  is_admin = models.CharField(max_length=5, default='false')

  class Meta:
    unique_together = [['room', 'person']]

  def __str__(self):
    return self.person.first_name + ' ' + self.person.last_name 



class Channel(models.Model):

  """ A model for creating channels inside a room """

  STATUS_CHANNEL = (
    ('private', 'Private'),
    ('public', 'Public'),
  )

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='all_channels')
  name = models.CharField(max_length=255)
  slug = AutoSlugField(populate_from='name')
  setting = models.CharField(choices=STATUS_CHANNEL, max_length=10, default='public')
  created_at = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ('name',)
    unique_together = [['name', 'room']]

  def __str__(self):
    return self.name


class PrivateChannelUser(models.Model):

  """ A  model for adding people to private channels """

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='private_channel_people')
  person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cc')
  joined = models.DateTimeField(auto_now_add=True)


  class Meta:
    unique_together = [['channel', 'person']]

  def __str__(self):
    return self.channel.name + ' ' + self.person.first_name + ' ' + self.person.last_name 
  



class MessagesInChannel(models.Model):

  """ A model for creating messages inside a channel """

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='all_messages')
  person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_messages')
  message = RichTextUploadingField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ('created_at',)

  def __str__(self):
    return SafeString(self.message)



