from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from loguru import logger

from .models import *
from .models import PlayerClass


@login_required
def CreateRoomViews(request):
    type_room = request.POST.get("type_room")
    leavel_to_win = request.POST.get("leavel_to_win")
    rules_book = request.user.rulesBook.all().filter(
        pk=request.POST.get("rules_book")).first()
    room = Rooms.objects.create(room_type=type_room, leavel_to_win=leavel_to_win,
                                rules_book=rules_book, admin=request.user, owner=request.user)
    RoomPlayer.objects.create(
        room=room, player=request.user, order=1, gender=request.user.gender)
    return HttpResponseRedirect(reverse('room', args=(room.code,)))


@login_required
def StopRoomViews(request, room_code):
    room = Rooms.objects.get(code=room_code, admin=request.user)
    logger.debug('Hellooo')
    room.end = True
    room.save()
    logger.debug('Hellooo')
    return HttpResponseRedirect(reverse('profile'))


@login_required
def RoomViews(request, room_code=None):
    if room_code:
        room = get_object_or_404(Rooms, code=room_code)
    else:
        room = ''
    context = {
        "title": f"Комната",
        'room': room,
        'classes': PlayerClass.CLASS_CHOICES,
        'races': PlayerRace.CLASS_CHOICES,
    }
    return render(request, 'room/room.html', context)


@login_required
def update_player_class(request, player_id, class_value):
    player = RoomPlayer.objects.get(pk=player_id)
    player_class = player.playerClass.last()

    # Установите новое значение класса игрока
    player_class.value = class_value
    player_class.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def update_player_race(request, player_id, race_value):
    player = RoomPlayer.objects.get(pk=player_id)
    player_race = player.playerRace.last()

    # Установите новое значение класса игрока
    player_race.value = race_value
    player_race.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
