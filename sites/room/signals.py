import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PlayerLeavel, PlayerPower, RoomPlayer


@receiver(post_save, sender=PlayerLeavel)
def create_player_level(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            settings.LEVEL_GROUP_NAME, {
                "type": 'new_level',
                "content": json.dumps({'level': instance.leavel, 'playerId': instance.player.id}),
            })


@receiver(post_save, sender=PlayerPower)
def create_player_power(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            settings.POWER_GROUP_NAME, {
                "type": 'new_power',
                "content": json.dumps({'power': instance.power, 'playerId': instance.player.id}),
            })
