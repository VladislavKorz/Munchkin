from django.http import HttpResponse, HttpResponseNotFound
from loguru import logger
import json

from .models import *

def changeRoomPlayerAjax(request):
    if request.POST:
        logger.debug(request.POST)
        status = 400
        status_message = 'Нет информации'
        user_room = RoomPlayer.objects.get(pk=request.POST.get('user_room'))
        if request.POST.get('gender'):
            user_room.gender = request.POST.get('gender')
            user_room.save()
            status = 200
            status_message = 'Ok'
        if request.POST.get('data'):
            status = 200
            status_message = 'Ok'
            data = json.loads(request.POST.get('data'))
            if data.get('power') or data.get('level'):
                leavel = PlayerLeavel.objects.filter(player=user_room).first()
                power = PlayerPower.objects.filter(player=user_room).first()
                if data.get('level') and data.get('level') != leavel.leavel:
                    PlayerLeavel.objects.create(player=user_room, leavel = data.get('level'))
                if data.get('power') and data.get('power') != power.power:
                    PlayerPower.objects.create(player=user_room, power = data.get('power'))


        return HttpResponse(json.dumps({'message':status_message}), content_type='application/json', status=status)
    else:
        return HttpResponseNotFound('Страница не найдена или не верный запрос')