# django Apps
from django.urls import path

# Current App Modules
from .views import MyCreatedRoomAPIView, CreateARoomAPIView, SearchByNameAPIView, CreateChannelAPIView, CreateMessageAPIView, AddPeopleToRoomAPIView, AddPeopleToRoomAPIView, ShowUsersInRoomAPIView, ShowChannelsInRoomAPIView, ShowMessagesInChannelAPIView,  CreateMessageAPIView, ShowRoomDetailAPIView, GetUserByIdAPIView, DeleteRoomAPIView, UpdateRoomAPIView, DeleteChannelInRoomAPIView, UpdateChannelInRoomAPIView, DeletePeopleInRoomAPIView, SearchMessageAPIView, ShowChannelDetailAPIView, DeleteMessageAPIView, DeletePeopleInRoomAPIView, MyRoomAPIView, UpdateMessageInChannelAPIView, ShowMessageDetailAPIView, AddDescriptionToRoomAPIView, AddPeopleToPrivateChannelAPIView, DeletePeopleInPrivateChannelAPIView, ShowUsersInPrivateChannel

""" Collaborative Application URL Endpoints for Holograph """


urlpatterns = [

    path('room_i_belong_to/', MyRoomAPIView.as_view()),


    path('my_created_room/', MyCreatedRoomAPIView.as_view()),
 

    path('create_a_room/<str:title>/', CreateARoomAPIView.as_view()),


    path('add_description_to_room/<uuid:room_id>/<str:description>/', AddDescriptionToRoomAPIView.as_view()),

 
    path('search_person/<str:name>/', SearchByNameAPIView.as_view()),


    path('add_people_to_room/<uuid:room_id>/<int:person_id>/', AddPeopleToRoomAPIView.as_view()),


    path('create_a_channel/<uuid:room_id>/<str:name>/<str:setting>/', CreateChannelAPIView.as_view()),


    path('add_people_to_private_channel/<uuid:room_id>/<uuid:channel_id>/<int:person_id>/', AddPeopleToPrivateChannelAPIView.as_view()),


    path('show_users_in_room/<uuid:room_id>/', ShowUsersInRoomAPIView.as_view()),


    path('show_channel_in_room/<uuid:room_id>/', ShowChannelsInRoomAPIView.as_view()),


    path('show_room/<uuid:pk>/', ShowRoomDetailAPIView.as_view()),


    path('show_channel/<uuid:pk>/', ShowChannelDetailAPIView.as_view()),


    path('show_message/<uuid:pk>/', ShowMessageDetailAPIView.as_view()),


    path('show_messages_in_channel/<uuid:room_id>/<uuid:channel_id>/', ShowMessagesInChannelAPIView.as_view()),


    path('show_people_in_private_channel/<uuid:channel_id>/', ShowUsersInPrivateChannel.as_view()),


    path('create_a_message/<uuid:room_id>/<uuid:channel_id>/<int:person_id>/<str:message>/', CreateMessageAPIView.as_view()),


    path('get_user_by_id/<int:pk>/', GetUserByIdAPIView.as_view()),


    path('search_message/<uuid:room_id>/<uuid:channel_id>/<str:message>/', SearchMessageAPIView.as_view()),


    path('delete_room/<uuid:room_id>/', DeleteRoomAPIView.as_view()),


    path('delete_message_in_channel/<uuid:message_id>/', DeleteMessageAPIView.as_view()),


    path('delete_channel_in_room/<uuid:room_id>/<uuid:channel_id>/', DeleteChannelInRoomAPIView.as_view()),


    path('delete_people_in_room/<uuid:room_id>/<int:person_id>/', DeletePeopleInRoomAPIView.as_view()),


    path('delete_people_in_private_channel/<uuid:room_id>/<uuid:channel_id>/<int:person_id>/', DeletePeopleInPrivateChannelAPIView.as_view()),


    path('update_channel_in_room/<uuid:room_id>/<uuid:channel_id>/<str:new_name>/<str:new_setting>', UpdateChannelInRoomAPIView.as_view()),


    path('update_room/<uuid:room_id>/<str:new_title>/', UpdateRoomAPIView.as_view()),


    path('update_message_in_channel/<uuid:message_id>/<str:new_message>/', UpdateMessageInChannelAPIView.as_view()),
 
    

]
