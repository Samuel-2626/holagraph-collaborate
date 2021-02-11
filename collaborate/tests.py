from django.test import TestCase
from django.contrib.auth.models import User

from channels.testing import WebsocketCommunicator


from .models import Room, People, Channel, MessagesInChannel



""""
  This is are series test to ensure that a logged-in user can create a(room, people, channel and message)
"""


class RoomTest(TestCase):

  @classmethod
  def setUpTestData(cls):
    # Create a user
    testuser1 = User.objects.create_user(
      username='testuser1', password='abc123'
    )
    testuser1.save()

    # Create a new room
    test_room = Room.objects.create(
      title='Room title', created_by=testuser1
    )

    test_room.save()

  def test_room_content(self):
    room = Room.objects.get()

    title = f'{room.title}'
    created_by = f'{room.created_by}'

    self.assertEqual(created_by, 'testuser1')
    self.assertEqual(title, 'Room title')



class PeopleTest(TestCase):

  @classmethod
  def setUpTestData(cls):
    # Create a user
    testuser1 = User.objects.create_user(
      username='testuser1', password='abc123'
    )
    testuser1.save()

    # Create a new room
    test_room = Room.objects.create(
      title='Room title', created_by=testuser1
    )

    test_room.save()

    #  Add people to room 
    test_people = People.objects.create(
      room=test_room, person=testuser1
    )

    test_people.save()


  def test_people_content(self):
    people = People.objects.get()

    room = f'{people.room}'
    person = f'{people.person}'

    self.assertEqual(room, 'Room title')
    self.assertEqual(person, 'testuser1')



class ChannelTest(TestCase):

  @classmethod
  def setUpTestData(cls):

    # Create a user
    testuser1 = User.objects.create_user(
      username='testuser1', password='abc123'
    )
    testuser1.save()
    
    # Create a new room
    test_room = Room.objects.create(
      title='Room title', created_by=testuser1
    )

    test_room.save()

    #  Create a new channel
    test_channel = Channel.objects.create(
      room=test_room, name='Channel Name'
    )

    test_channel.save()


  def test_channel_content(self):
    channel = Channel.objects.get()

    room = f'{channel.room}'
    name = f'{channel.name}'

    self.assertEqual(room, 'Room title')
    self.assertEqual(name, 'Channel Name')




class MessageTest(TestCase):

  @classmethod
  def setUpTestData(cls):

    # Create a user
    testuser1 = User.objects.create_user(
      username='testuser1', password='abc123'
    )
    testuser1.save()
    
    # Create a new room
    test_room = Room.objects.create(
      title='Room title', created_by=testuser1
    )

    test_room.save()

    # Create a new channel
    test_channel = Channel.objects.create(
      room=test_room, name='Channel Name'
    )

    test_channel.save()

    # Create a new message
    test_message = MessagesInChannel.objects.create(
      channel=test_channel, person=testuser1, message='Test Message'
    )

    test_message.save()

    

  def test_channel_content(self):
    messageInChannel = MessagesInChannel.objects.get()

    channel = f'{messageInChannel.channel}'
    person = f'{messageInChannel.person}'
    message = f'{messageInChannel.message}'

    self.assertEqual(channel, 'Channel Name')
    self.assertEqual(person, 'testuser1')
    self.assertEqual(message, 'Test Message')


