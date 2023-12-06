import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import (ConnectionRequest, PlayerLeavel, PlayerPower, RoomPlayer,
                     Rooms, get_code)


@receiver(post_save, sender=PlayerLeavel)
def create_player_level(sender, instance, created, **kwargs):
    created_at = instance.create
    if instance.creator==None:
        creator = instance.player.player.username
    else:
        creator = instance.creator.username
    if created:
        try:
            power = instance.player.get_power()
        except:
            power = 0
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            settings.LEVEL_GROUP_NAME, {
                "type": 'new_level',
                "content": json.dumps({'creator': creator, 'level': instance.leavel, 'playerId': instance.player.id, 'power': power, 'username': instance.player.player.username, 'date': created_at.strftime("%d.%m"), 'time': created_at.strftime("%H:%M"), 'room': instance.player.room.code}),
            })


@receiver(post_save, sender=PlayerPower)
def create_player_power(sender, instance, created, **kwargs):
    created_at = instance.create
    if instance.creator==None:
        creator = instance.player.player.username
    else:
        creator = instance.creator.username
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            settings.POWER_GROUP_NAME, {
                "type": 'new_power',
                "content": json.dumps({'creator': creator, 'power': instance.power, 'playerId': instance.player.id, 'level': instance.player.get_leavel(), 'username': instance.player.player.username, 'date': created_at.strftime("%d.%m"), 'time': created_at.strftime("%H:%M"), 'room': instance.player.room.code}),
            })


@receiver(pre_save, sender=RoomPlayer)
def room_player_gender_changed(sender, instance, **kwargs):
    if instance.id:
        previous = RoomPlayer.objects.get(id=instance.id)
        if previous.gender != instance.gender:
            print('test')
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                settings.GENDER_GROUP_NAME, {
                    "type": 'new_gender',
                    "content": json.dumps({'last_request_user': instance.last_request_user.username, 'gender': instance.gender, 'playerId': instance.id, 'username': instance.player.username, 'gender_display': instance.get_gender_display()}),
                })


@receiver(pre_save, sender=Rooms)
def set_unique_code(sender, instance, **kwargs):
    previous = Rooms.objects.filter(id=instance.id).first()
    if previous:
        instance.code = previous.code



@receiver(post_save, sender=ConnectionRequest)
def create_player_connection(sender, instance, created, **kwargs):
    created_at = instance.create
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            settings.CONNECTION_REQUEST_GROUP_NAME, {
                "type": 'new_connection_request',
                "content": json.dumps({'connectionID': instance.id, 'code': instance.room.code, 'playerId': instance.player.id, 'username': instance.player.username, 'created_at': created_at.strftime("%H:%M %d.%m"), 'spectator': instance.spectator}),
            })


@receiver(post_save, sender=ConnectionRequest)
def create_player_connection(sender, instance, created, **kwargs):
    if instance.approved:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            settings.APPROVE_CONNECTION_GROUP_NAME, {
                "type": 'approve_connection_request',
                "content": json.dumps({'connectionID': instance.id, 'code': instance.room.code, 'playerId': instance.player.id, 'username': instance.player.username}),
            })


@receiver(post_save, sender=RoomPlayer)
def create_room_player(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            settings.ROOM_PLAYER_GROUP_NAME, {
                "type": 'new_room_player',
                "content": json.dumps({'absolute_url':instance.player.get_absolute_url(), 'code':instance.room.code, 'gender': instance.gender, 'playerId': instance.id, 'username': instance.player.username, 'gender_display': instance.get_gender_display(), 'level': instance.get_leavel(), 'power': instance.get_power(), 'image': instance.player.get_photo_url(), 'race': instance.get_racer(), 'class': instance.get_class()}),
            })
