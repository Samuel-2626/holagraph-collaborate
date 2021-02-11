# third-party libraries
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotAcceptable
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.renderers import JSONRenderer, MultiPartRenderer, BrowsableAPIRenderer
from rest_framework import status

# django apps
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.core.mail import send_mail

# django modules
from collaborate.models import Room, People, Channel, MessagesInChannel, PrivateChannelUser

# current app modules
from .serializers import MyCreatedRoomSerializer, SearchByNameSerializer, ShowUsersInRoomSerializer, ShowChannelsInRoomSerializer, ShowMessagesInChannelSerializer, ShowRoomDetailSerializer, GetUserByIdSerializer, SearchMessageSerializer,ShowChannelDetailSerializer, MyRoomSerializer, ShowMessageDetailSerializer, ShowUsersInPrivateChannelSerializer

from .permissions import IsCreatedMessage, IsCreatedRoom, IsCreatedChannel, IsMemberOfRoom



""" Collaborative Application View (Business Logic) for Holograph """



class MyRoomAPIView(generics.ListAPIView):
 

  serializer_class = MyRoomSerializer

  def get_queryset(self):
    """
      This view should return a list of all the rooms belonging to the currently authenticated user
    """
    user = self.request.user
    return People.objects.filter(person=user)

  



class MyCreatedRoomAPIView(generics.ListAPIView):

  serializer_class = MyCreatedRoomSerializer

  def get_queryset(self):
    """
      This view should return a list of all the rooms created for the currently authenticated user
    """
    user = self.request.user
    return Room.objects.filter(created_by=user)



class CreateARoomAPIView(APIView):
  def post(self, request, title, format=None):

    room = Room(title=title, created_by=request.user)
    try:
      room.save()

      people = People(room=room, person=request.user, is_admin='true')

      people.save()

    except:
      raise NotAcceptable('This Room already exists')

    return Response({'Successfully Added': True})



class AddDescriptionToRoomAPIView(APIView):

  def post(self, request, room_id, description, format=None):

    new_room = get_object_or_404(Room, pk=room_id)


    if new_room.created_by == request.user:

      new_room.description = description
      
      try:
        new_room.save()

      except:
        raise NotAcceptable('Error Adding Description, Please try again later')

      return Response({'Successfully Added': True})

    else:
      raise PermissionDenied('Access Denied, You are not the author of this room')

  


class SearchByNameAPIView(generics.ListAPIView):

  serializer_class = SearchByNameSerializer

  def get_queryset(self):
    """
      This view should return a list of all the fullname for
      the user as determined by the name portion of the URL.
    """
    name = self.kwargs['name']
    return User.objects.filter(first_name__icontains=name).exclude(email__icontains=self.request.user.email) or User.objects.filter(last_name__icontains=name).exclude(email__icontains=self.request.user.email)


class AddPeopleToRoomAPIView(APIView):

  def post(self, request, room_id, person_id ,format=None):

    room = get_object_or_404(Room, pk=room_id)

    person = get_object_or_404(User, pk=person_id)

    if room.created_by == request.user:
      
      people = People(room=room, person=person)

      try:
        people.save()

        # Send an email to the user address + plus a link to enter room
        send_mail('Holagraph: IndiaClap Platform', f'You have being added to {room.title} room on Holagraph web application \n\n Thank you \n\n Holagraph Team ', 'info@reach.com', [person.email,])

      except:
        raise NotAcceptable('This User already exists')
      return Response({'Successfully Added': True})

    else:
      return Response({'Rejected': 'Access Denied, You are not the author of this room'}, status=403)


  


class CreateChannelAPIView(APIView):

  def post(self, request, room_id, name, setting, format=None):
    room = get_object_or_404(Room, pk=room_id)

    channel = Channel(room=room, name=name, setting=setting)

    if setting == 'private':
      private_channel = PrivateChannelUser(channel=channel, person=request.user)
      

    if room.created_by == request.user:
      
      try:
        channel.save()
        private_channel.save()
      except:
        raise NotAcceptable('This Channel already exists')
      return Response({'Successfully Added': True})

    else:
      return Response({'Rejected': 'Access Denied, You are not the author of this room'}, status=403)



class AddPeopleToPrivateChannelAPIView(APIView):

  def post(self, request, room_id, channel_id, person_id, format=None):
    room = get_object_or_404(Room, pk=room_id)

    channel = get_object_or_404(Channel, pk=channel_id)

    if channel.setting == 'public':
      return Response({'Rejected': 'Access Denied, This is a public channel'}, status=403)


    person = get_object_or_404(User, pk=person_id)

    private_person = PrivateChannelUser(person=person, channel=channel)

    if room.created_by == request.user:
      
      try:
        private_person.save()
      except:
        raise NotAcceptable('This Person already exists')
      return Response({'Successfully Added': True})

    else:
      return Response({'Rejected': 'Access Denied, You are not the author of this room'}, status=403)




class ShowUsersInRoomAPIView(generics.ListAPIView):


  serializer_class = ShowUsersInRoomSerializer

  def get_queryset(self):
    """
      This view should return a list of all the users for a particular room
    """
    room = self.kwargs['room_id']

    if People.objects.filter(room__pk=room, person=self.request.user):
      return People.objects.filter(room__pk=room)
    
    else:
      raise PermissionDenied('Access Denied, You are not a member of this room')    



class ShowChannelsInRoomAPIView(generics.ListAPIView):

  serializer_class = ShowChannelsInRoomSerializer

  def get_queryset(self):
    """
      This view should return a list of all the channels created for a particular room
    """
    room = self.kwargs['room_id']

    if People.objects.filter(room__pk=room, person=self.request.user):
      return Channel.objects.filter(room__pk=room)
    
    else:
      raise PermissionDenied('Access Denied, You are not a member of this room')



class ShowUsersInPrivateChannel(generics.ListAPIView):

  serializer_class = ShowUsersInPrivateChannelSerializer

  def get_queryset(self):
      
    channel = self.kwargs['channel_id']

    if PrivateChannelUser.objects.filter(person=self.request.user, channel__pk=channel):
      return PrivateChannelUser.objects.filter(channel__pk=channel)
    
    else:
      raise PermissionDenied('Access Denied, You are not a member of this private room')    
  



class ShowRoomDetailAPIView(generics.RetrieveAPIView):

  queryset = Room.objects.all()
  serializer_class = ShowRoomDetailSerializer



class ShowChannelDetailAPIView(generics.RetrieveAPIView):

  queryset = Channel.objects.all()
  serializer_class = ShowChannelDetailSerializer


class ShowMessageDetailAPIView(generics.RetrieveAPIView):

  queryset = MessagesInChannel.objects.all()
  serializer_class = ShowMessageDetailSerializer



class ShowMessagesInChannelAPIView(generics.ListAPIView):
  renderer_classes = (BrowsableAPIRenderer, JSONRenderer, MultiPartRenderer)
  serializer_class = ShowMessagesInChannelSerializer

  def get_queryset(self):
    """
      This view should return a list of all the rooms created for the currently authenticated user
    """
    channel = self.kwargs['channel_id']
    room = self.kwargs['room_id']

    if People.objects.filter(room__pk=room, person=self.request.user):
      return MessagesInChannel.objects.filter(channel__pk=channel)
    
    else:
      raise PermissionDenied('Access Denied, You are not a member of this room')
    

class CreateMessageAPIView(APIView):
  parser_classes = (FormParser, MultiPartParser)
  def post(self, request, room_id, channel_id, person_id, message, format=None):
    channel = get_object_or_404(Channel, pk=channel_id)
    person = get_object_or_404(User, pk=person_id)

    if People.objects.filter(room__pk=room_id, person=request.user):

      message = MessagesInChannel(channel=channel, person=person, message=message)
      try:
        message.save()
      except:
        raise NotAcceptable('Sorry a problem occurred, please try again later')
      return Response({'Successfully Added': True})
    
    else:
      raise PermissionDenied('Access Denied, You are not a member of this room')



class GetUserByIdAPIView(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = GetUserByIdSerializer



class SearchMessageAPIView(generics.ListAPIView):

  serializer_class = SearchMessageSerializer

  def get_queryset(self):
    """
      This view should return a list of all the messages for
      the channel as determined by the message and channel portion of the URL.
    """
    channel = self.kwargs['channel_id']
    message = self.kwargs['message']
    room = self.kwargs['room_id']

    if People.objects.filter(room__pk=room, person=self.request.user):
      return MessagesInChannel.objects.filter(channel__pk=channel).filter(message__icontains=message)
    
    else:
      raise PermissionDenied('Access Denied, You are not a member of this room')



class DeleteRoomAPIView(APIView):

  def delete(self, request, room_id, format=None):

    room = get_object_or_404(Room, pk=room_id)


    if room.created_by == request.user:

      try:
        room.delete()
      except:
        raise NotAcceptable('An error occurred, please try again later')
      return Response({'Successfully Deleted': True})

    else:
      raise PermissionDenied('Access Denied, You are not the creator of this room')

  


class DeleteMessageAPIView(APIView):

  def delete(self, request, message_id, format=None):

    my_message = get_object_or_404(MessagesInChannel, pk=message_id)

    if my_message.person == request.user:
      my_message.delete()
      try:
        pass
      except:
        raise NotAcceptable('An error occurred, please try again later')
      return Response({'Successfully Deleted': True})

    else:
      raise PermissionDenied('Access Denied, You are not the author of this message')


class DeleteChannelInRoomAPIView(APIView):

  def delete(self, request, room_id, channel_id, format=None):

    room = get_object_or_404(Room, pk=room_id)
    channel = get_object_or_404(Channel, pk=channel_id)


    if room.created_by == request.user:

      try:
        channel.delete()
      except:
        raise NotAcceptable('An error occurred, please try again later')
      return Response({'Successfully Deleted': True})

    else:
      raise PermissionDenied('Access Denied, You are not the creator of this room')


class DeletePeopleInRoomAPIView(APIView):
  
  def delete(self, request, room_id, person_id, format=None):

    room = get_object_or_404(Room, pk=room_id)
    people = get_object_or_404(People, room=room, person=person_id)

    if room.created_by == people.person:
      return Response({'Rejected': 'Access Denied, You can\'t exist this room'}, status=403)

    if room.created_by == request.user:

      try:
        people.delete()
      except:
        raise NotAcceptable('An error occurred, please try again later')
      return Response({'Successfully Deleted': True})

    else:
      raise PermissionDenied('Access Denied, You are not the creator of this room')


class DeletePeopleInPrivateChannelAPIView(APIView):
  
  def delete(self, request, room_id, channel_id, person_id, format=None):

    room = get_object_or_404(Room, pk=room_id)
    channel = get_object_or_404(Channel, pk=channel_id)
    person = get_object_or_404(User, pk=person_id)
    private_person = get_object_or_404(PrivateChannelUser, channel=channel, person=person)

    if room.created_by == private_person.person:
      return Response({'Rejected': 'Access Denied, You can\'t exist this private channel'}, status=403)

    if room.created_by == request.user:

      try:
        private_person.delete()
      except:
        raise NotAcceptable('An error occurred, please try again later')
      return Response({'Successfully Deleted': True})

    else:
      raise PermissionDenied('Access Denied, You are not the creator of this room')



class UpdateRoomAPIView(APIView):

  def post(self, request, room_id, new_title, format=None):

    new_room = get_object_or_404(Room, pk=room_id)


    if new_room.created_by == request.user:

      new_room.title = new_title
      
      try:
        new_room.save()
        
      except IntegrityError:
        raise NotAcceptable('This Room already exists')

      except:
        raise NotAcceptable('Error Updating, Please try again later')

      return Response({'Successfully Updated': True})

    else:
      raise PermissionDenied('Access Denied, You are not the creator of this room')



class UpdateChannelInRoomAPIView(APIView):
  
  def post(self, request, room_id, channel_id, new_name, new_setting, format=None):

    room = get_object_or_404(Room, pk=room_id)
    new_channel = get_object_or_404(Channel, pk=channel_id)

    new_channel.name = new_name
    new_channel.setting = new_setting

    if room.created_by == request.user:
      
      try:
        new_channel.save()
      except:
        raise NotAcceptable('This Channel already exists')
      return Response({'Successfully Updated': True})

    else:
      raise PermissionDenied('Access Denied, You are not the creator of this room')


class UpdateMessageInChannelAPIView(APIView):
  
  def post(self, request, message_id, new_message, format=None):

    message = get_object_or_404(MessagesInChannel, pk=message_id)

    message.message = new_message


    if message.person == request.user:
      
      try:
        message.save()
      except:
        raise NotAcceptable('An error occurred, please try again later')
      return Response({'Successfully Updated': True})

    else:
      raise PermissionDenied('Access Denied, You are not the creator of this message')
 

