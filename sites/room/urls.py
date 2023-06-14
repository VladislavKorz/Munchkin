from django.contrib import admin
from django.urls import path, include
from .views import *
from .ajaxViews import *

urlpatterns = [
    path('create/', CreateRoomViews, name='createRoom'),
    path('stop/<str:room_code>', StopRoomViews, name='stopRoom'),
    
    path('ajax/change_roomPlayer/', changeRoomPlayerAjax, name='ajax_changeRoomPlayer'),
    path('<str:room_code>/', RoomViews, name='room'),

]
