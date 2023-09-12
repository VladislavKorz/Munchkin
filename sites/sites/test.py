# import json

# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# from django.conf import settings


# def broadcast_ticks(ticks):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         settings.TICKS_GROUP_NAME, {
#             "type": 'new_ticks',
#             "content": ticks,
#         })


# ticks = 'USD'
