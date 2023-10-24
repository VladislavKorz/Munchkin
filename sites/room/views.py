import json
import random

import qrcode
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import F
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from loguru import logger
from meta.models import MetaTag

from .models import *
from .models import PlayerClass


def broadcast_race(race, player_id, username, date, time, room):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        settings.RACE_GROUP_NAME, {
            "type": 'new_race',
            "content": json.dumps({'race': race, 'playerId': player_id, 'username': username, 'date': date, 'time': time, 'room': room}),
        })

def broadcast_class(player_class, player_id, username, date, time, room):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        settings.CLASS_GROUP_NAME, {
            "type": 'new_class',
            "content": json.dumps({'class': player_class, 'playerId': player_id, 'username': username, 'date': date, 'time': time, 'room': room}),
        })

@login_required
def CreateRoomViews(request):
    type_room = request.POST.get("type_room")
    leavel_to_win = request.POST.get("leavel_to_win")
    rules_book = request.user.rulesBook.all().filter(
        pk=request.POST.get("rules_book")).first()
    only_verified_users = request.POST.get("email_verified") == "on"
    room = Rooms.objects.create(room_type=type_room, leavel_to_win=leavel_to_win,
                                rules_book=rules_book, admin=request.user, owner=request.user, only_verified_users=only_verified_users)
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

    if room.only_verified_users and not request.user.email_verify:
        return render(request, 'room/email_confirm.html')

    if room.room_type == 'C' and room.owner!=request.user:
        return render(request, 'room/solo_room_error.html')

    context = {
        "title": f"Комната-{room.code}",
        'connections': room.connection.filter(approved=False, create=F('update')).order_by('-create'),
        'room': room,
        'connection_requests': ConnectionRequest.objects.filter(room__code=room_code),
        'classes': PlayerClass.CLASS_CHOICES,
        'races': PlayerRace.CLASS_CHOICES,
    }
    return render(request, 'room/room.html', context)



@login_required
def update_player_class(request, player_id, class_value, class_name):
    player = RoomPlayer.objects.get(pk=player_id)

    player_class = PlayerClass.objects.create(player=player, value=class_value)
    created_at = player_class.create
    broadcast_class(class_name, player_id, player.player.username, created_at.strftime("%d.%m"), created_at.strftime("%H:%M"), player.room.code)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def update_player_race(request, player_id, race_value, race_name):
    player = RoomPlayer.objects.get(pk=player_id)

    race = PlayerRace.objects.create(player=player, value=race_value)
    created_at = race.create
    broadcast_race(race_name, player_id, player.player.username, created_at.strftime("%d.%m"), created_at.strftime("%H:%M"), player.room.code)

    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return JsonResponse({'message': 'Данные успешно обновлены'})


def generate_qr_code(request, room_code):
    # Создаем объект QR-кода
    qr = qrcode.QRCode(
        version=1,  # Размер QR-кода
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Уровень коррекции ошибок
        box_size=5,  # Размер каждого "блока" QR-кода
        border=4,    # Количество блоков вокруг QR-кода
    )

    # Генерируем URL для QR-кода
    room_url = reverse('make_qr_connection_request', args=[room_code])
    url = request.build_absolute_uri(room_url)

    # Добавляем данные в QR-код
    qr.add_data(url)
    qr.make(fit=True)

    # Создаем изображение QR-кода
    img = qr.make_image(fill_color="blue", back_color="white")

    # Сохраняем изображение или отдаем как HttpResponse
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response




def simple_chart_view(request):
    room = Rooms.objects.first()
    players = room.player.all()
    return render(request, 'room/test.html', {"players":players})


def statistics_view(request, code):
    template = 'room/statistics.html'
    room = get_object_or_404(Rooms, code=code)
    players = room.player.all()
    metatag = MetaTag.objects.get(html_path=template)
    return render(request, template, {'players': players, 'title': metatag.title, 'metatag': metatag})


def accept_connection(request, connection_id):
    connection = ConnectionRequest.objects.get(pk=connection_id)
    connection.approved = True
    connection.save()
    # Здесь можно добавить код для отправки сообщения о принятии запроса через WebSocket
    return HttpResponse("Запрос принят")

def reject_connection(request, connection_id):
    connection = ConnectionRequest.objects.get(pk=connection_id)
    connection.approved = False
    connection.save()
    # Здесь можно добавить код для отправки сообщения об отклонении запроса через WebSocket
    return HttpResponse("Запрос отклонен")
