from django.contrib import admin
from django.urls import include, path

from .ajaxViews import *
from .views import *

urlpatterns = [
    path('create/', CreateRoomViews, name='createRoom'),
    path('stop/<str:room_code>', StopRoomViews, name='stopRoom'),

    path('ajax/change_roomPlayer/', changeRoomPlayerAjax, name='ajax_changeRoomPlayer'),
    path('<str:room_code>/', RoomViews, name='room'),
    path('update_player_class/<int:player_id>/<str:class_value>/<str:class_name>/', update_player_class, name='update_player_class'),
    path('update_player_race/<int:player_id>/<str:race_value>/<str:race_name>/', update_player_race, name='update_player_race'),
    path('generate_qr_code/<str:room_code>/', generate_qr_code, name='generate_qr_code'),
    path('statistics/<str:code>/', statistics_view, name='statistics'),
    path('accept_connection/<int:connection_id>/', accept_connection, name='accept_connection'),
    path('reject_connection/<int:connection_id>/', reject_connection, name='reject_connection'),
]
