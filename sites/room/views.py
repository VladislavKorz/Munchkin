from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from loguru import logger
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *


@login_required
def CreateRoomViews(request):
    type_room = request.POST.get("type_room")
    leavel_to_win = request.POST.get("leavel_to_win")
    rules_book = request.user.profile.rulesBook.all().filter(pk=request.POST.get("rules_book")).first()
    Rooms.objects.create(room_type=type_room, leavel_to_win=leavel_to_win, rules_book=rules_book, admin=request.user.profile, owner=request.user.profile)


@login_required
def RoomViews(request, room_code = None):
    if room_code:
        room = get_object_or_404(Rooms, code=room_code)
    else:
        room = ''
    context = {
        "title": f"Комната",
        'room': room,
    }
    return render(request, 'room/room.html', context)