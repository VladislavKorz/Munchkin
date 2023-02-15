from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('create/', CreateRoomViews, name='createRoom'),
    path('<str:room_code>/', RoomViews, name='room'),
]
