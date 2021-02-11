from django.contrib import admin
from .models import Room, Channel, MessagesInChannel, People, PrivateChannelUser

# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'description', 'created_by', 'created_at', 'updated')
  list_filter = ('created_by', 'created_at')
  search_fields = ('title', 'description')
  raw_id_fields = ('created_by',)
  date_hierarchy = 'created_at'
  ordering = ('created_by',)

@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
  list_display = ('person', 'joined', 'room', 'is_admin')
  list_filter = ('joined', 'person')
  search_fields = ('person',)
  raw_id_fields = ('person', 'room')
  date_hierarchy = 'joined'
  ordering = ('joined',)

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'created_at', 'setting', 'room', 'updated')
  list_filter = ('created_at',)
  search_fields = ('name',)
  raw_id_fields = ('room',)
  date_hierarchy = 'created_at'
  ordering = ('created_at',)

@admin.register(PrivateChannelUser)
class PrivateChannelUserAdmin(admin.ModelAdmin):
  list_display = ('id', 'person', 'channel', 'joined')
  list_filter = ('joined', 'channel')
  search_fields = ('person',)
  raw_id_fields = ('person', 'channel')
  date_hierarchy = 'joined'
  ordering = ('joined',)

@admin.register(MessagesInChannel)
class MessagesInChannelAdmin(admin.ModelAdmin):
  list_display = ('id', 'message', 'created_at', 'person', 'channel', 'updated')
  list_filter = ('created_at',)
  search_fields = ('message', 'file')
  raw_id_fields = ('person', 'channel')
  date_hierarchy = 'created_at'
  ordering = ('created_at',)