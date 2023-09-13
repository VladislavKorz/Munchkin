import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import PlayerLeavel, PlayerPower, RoomPlayer


@receiver(post_save, sender=PlayerLeavel)
def create_player_level(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            settings.LEVEL_GROUP_NAME, {
                "type": 'new_level',
                "content": json.dumps({'level': instance.leavel, 'playerId': instance.player.id, 'power': instance.player.get_power()}),
            })


@receiver(post_save, sender=PlayerPower)
def create_player_power(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            settings.POWER_GROUP_NAME, {
                "type": 'new_power',
                "content": json.dumps({'power': instance.power, 'playerId': instance.player.id, 'level': instance.player.get_leavel()}),
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
                    "content": json.dumps({'gender': instance.gender, 'playerId': instance.id}),
                })
