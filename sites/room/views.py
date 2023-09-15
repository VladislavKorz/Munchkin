import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from loguru import logger

from .models import *
from .models import PlayerClass


def broadcast_race(race, player_id, username, date, time):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        settings.RACE_GROUP_NAME, {
            "type": 'new_race',
            "content": json.dumps({'race': race, 'playerId': player_id, 'username': username, 'date': date, 'time': time}),
        })

def broadcast_class(player_class, player_id, username, date, time):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        settings.CLASS_GROUP_NAME, {
            "type": 'new_class',
            "content": json.dumps({'class': player_class, 'playerId': player_id, 'username': username, 'date': date, 'time': time}),
        })

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
def update_player_class(request, player_id, class_value, class_name):
    player = RoomPlayer.objects.get(pk=player_id)

    player_class = PlayerClass.objects.create(player=player, value=class_value)
    created_at = player_class.create
    broadcast_class(class_name, player_id, player.player.username, created_at.strftime("%d.%m"), created_at.strftime("%H:%M"))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def update_player_race(request, player_id, race_value, race_name):
    player = RoomPlayer.objects.get(pk=player_id)

    race = PlayerRace.objects.create(player=player, value=race_value)
    created_at = race.create
    broadcast_race(race_name, player_id, player.player.username, created_at.strftime("%d.%m"), created_at.strftime("%H:%M"))

    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return JsonResponse({'message': 'Данные успешно обновлены'})
