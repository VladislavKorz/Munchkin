import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import PlayerLeavel, PlayerPower, RoomPlayer, Rooms, get_code


@receiver(post_save, sender=PlayerLeavel)
def create_player_level(sender, instance, created, **kwargs):
    created_at = instance.create
    if created:
        try:
            power = instance.player.get_power()
        except:
            power = 0
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            settings.LEVEL_GROUP_NAME, {
                "type": 'new_level',
                "content": json.dumps({'level': instance.leavel, 'playerId': instance.player.id, 'power': power, 'username': instance.player.player.username, 'date': created_at.strftime("%d.%m"), 'time': created_at.strftime("%H:%M")}),
            })


@receiver(post_save, sender=PlayerPower)
def create_player_power(sender, instance, created, **kwargs):
    created_at = instance.create
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            settings.POWER_GROUP_NAME, {
                "type": 'new_power',
                "content": json.dumps({'power': instance.power, 'playerId': instance.player.id, 'level': instance.player.get_leavel(), 'username': instance.player.player.username, 'date': created_at.strftime("%d.%m"), 'time': created_at.strftime("%H:%M")}),
            })


@receiver(pre_save, sender=RoomPlayer)
def room_player_gender_changed(sender, instance, **kwargs):
    print('test1')
    if instance.id:
        previous = RoomPlayer.objects.get(id=instance.id)
        if previous.gender != instance.gender:
            print('test')
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                settings.GENDER_GROUP_NAME, {
                    "type": 'new_gender',
                    "content": json.dumps({'gender': instance.gender, 'playerId': instance.id, 'username': instance.player.username, 'gender_display': instance.get_gender_display()}),
                })


@receiver(pre_save, sender=Rooms)
def set_unique_code(sender, instance, **kwargs):
    print('wut')
    previous = Rooms.objects.get(id=instance.id)
    if previous:
        instance.code = previous.code
