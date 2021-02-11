# third-party libraries
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

# django apps
from django.contrib.auth.models import User
from django.http import response


# django modules
from collaborate.models import Room, People, Channel, MessagesInChannel, PrivateChannelUser


""" Collaborative Application Serializer for Holograph """


class SearchByNameSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = "__all__"


class ShowRoomDetailSerializer(serializers.ModelSerializer):
  created_by = SearchByNameSerializer()
  class Meta:
    model = Room
    fields = ('id', 'title', 'description', 'slug', 'created_at', 'created_by')


class ShowChannelDetailSerializer(serializers.ModelSerializer):

  room = ShowRoomDetailSerializer()

  class Meta:
    model = Channel
    fields = ('id', 'room', 'name', 'created_at', 'setting')


class ShowMessageDetailSerializer(serializers.ModelSerializer):

  person = SearchByNameSerializer()
  channel = ShowChannelDetailSerializer()

  class Meta:
    model = MessagesInChannel
    fields = ('id', 'channel', 'person', 'message', 'created_at', 'updated')



class MyRoomSerializer(serializers.ModelSerializer):

  room = ShowRoomDetailSerializer()

  class Meta:
    model = People
    fields = ('room', 'joined', 'is_admin')   



class MyCreatedRoomSerializer(serializers.ModelSerializer):
  created_by = SearchByNameSerializer()
  class Meta:
    model = Room
    fields = ('id', 'title', 'description', 'created_at', 'created_by')



class ShowUsersInRoomSerializer(serializers.ModelSerializer):
  person = SearchByNameSerializer(read_only=False)
  class Meta:
    model = People
    fields = ('person', 'is_admin')


class ShowUsersInPrivateChannelSerializer(serializers.ModelSerializer):
  person = SearchByNameSerializer(read_only=False)
  channel = ShowChannelDetailSerializer()
  class Meta:
    model = PrivateChannelUser
    fields = ('id', 'person', 'joined', 'channel')



class ShowChannelsInRoomSerializer(serializers.ModelSerializer):

  class Meta:
    model = Channel
    fields = ('id', 'name', 'created_at', 'setting')




class ShowMessagesInChannelSerializer(serializers.ModelSerializer):
  person = SearchByNameSerializer()

  class Meta:
    model = MessagesInChannel
    fields = ('id', 'person', 'message', 'created_at')


class GetUserByIdSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = User
    fields = "__all__"


class SearchMessageSerializer(serializers.ModelSerializer):

  person = SearchByNameSerializer()
  class Meta:
    model = MessagesInChannel
    fields = ('id', 'person', 'message', 'created_at')


