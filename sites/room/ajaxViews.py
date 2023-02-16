from django.http import HttpResponse, HttpResponseNotFound
from loguru import logger
import json

from .models import RoomPlayer

def changeRoomPlayerAjax(request):
    if request.POST:
        logger.debug(request.POST)
        user_room = RoomPlayer.objects.get(pk=request.POST.get('user_room'))
        if request.POST.get('gender'):
            user_room.gender = request.POST.get('gender')
            user_room.save()
            status = 200
            status_message = 'Ok'
        return HttpResponse(json.dumps({'message':status_message}), content_type='application/json', status=status)
    else:
        return HttpResponseNotFound('Страница не найдена или не верный запрос')