from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from django.urls import reverse

from collaborate.models import Room, People, Channel, MessagesInChannel

# TODO