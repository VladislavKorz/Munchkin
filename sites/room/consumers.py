from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from django.conf import settings


class RaceSyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })

        # Join ticks group
        async_to_sync(self.channel_layer.group_add)(
            settings.RACE_GROUP_NAME,
            self.channel_name
        )

    def websocket_disconnect(self, event):
        # Leave ticks group
        async_to_sync(self.channel_layer.group_discard)(
            settings.RACE_GROUP_NAME,
            self.channel_name
        )

    def new_race(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['content'],
        })


class ClassSyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })

        # Join class group
        async_to_sync(self.channel_layer.group_add)(
            settings.CLASS_GROUP_NAME,  # Замените на имя вашей группы для классов
            self.channel_name
        )

    def websocket_disconnect(self, event):
        # Leave class group
        async_to_sync(self.channel_layer.group_discard)(
            settings.CLASS_GROUP_NAME,  # Замените на имя вашей группы для классов
            self.channel_name
        )

    def new_class(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['content'],
        })


class LevelSyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })

        # Join class group
        async_to_sync(self.channel_layer.group_add)(
            settings.LEVEL_GROUP_NAME,  # Замените на имя вашей группы для классов
            self.channel_name
        )

    def websocket_disconnect(self, event):
        # Leave class group
        async_to_sync(self.channel_layer.group_discard)(
            settings.LEVEL_GROUP_NAME,  # Замените на имя вашей группы для классов
            self.channel_name
        )

    def new_level(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['content'],
        })


class PowerSyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })

        # Join class group
        async_to_sync(self.channel_layer.group_add)(
            settings.POWER_GROUP_NAME,  # Замените на имя вашей группы для классов
            self.channel_name
        )

    def websocket_disconnect(self, event):
        # Leave class group
        async_to_sync(self.channel_layer.group_discard)(
            settings.POWER_GROUP_NAME,  # Замените на имя вашей группы для классов
            self.channel_name
        )

    def new_power(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['content'],
        })



class GenderSyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })

        # Join class group
        async_to_sync(self.channel_layer.group_add)(
            settings.GENDER_GROUP_NAME,  # Замените на имя вашей группы для классов
            self.channel_name
        )

    def websocket_disconnect(self, event):
        # Leave class group
        async_to_sync(self.channel_layer.group_discard)(
            settings.GENDER_GROUP_NAME,  # Замените на имя вашей группы для классов
            self.channel_name
        )

    def new_gender(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['content'],
        })


class ConnectionRequestSyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })

        # Join class group
        async_to_sync(self.channel_layer.group_add)(
            settings.CONNECTION_REQUEST_GROUP_NAME,  # Замените на имя вашей группы для классов
            self.channel_name
        )

    def websocket_disconnect(self, event):
        # Leave class group
        async_to_sync(self.channel_layer.group_discard)(
            settings.CONNECTION_REQUEST_GROUP_NAME,  # Замените на имя вашей группы для классов
            self.channel_name
        )

    def new_connection_request(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['content'],
        })


class ApproveConnectionRequestSyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })

        # Join class group
        async_to_sync(self.channel_layer.group_add)(
            settings.APPROVE_CONNECTION_GROUP_NAME,  # Замените на имя вашей группы для классов
            self.channel_name
        )

    def websocket_disconnect(self, event):
        # Leave class group
        async_to_sync(self.channel_layer.group_discard)(
            settings.CONNECTION_REQUEST_GROUP_NAME,  # Замените на имя вашей группы для классов
            self.channel_name
        )

    def approve_connection_request(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['content'],
        })



class RoomPlayerSyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })

        # Join ticks group
        async_to_sync(self.channel_layer.group_add)(
            settings.ROOM_PLAYER_GROUP_NAME,
            self.channel_name
        )

    def websocket_disconnect(self, event):
        # Leave ticks group
        async_to_sync(self.channel_layer.group_discard)(
            settings.ROOM_PLAYER_GROUP_NAME,
            self.channel_name
        )

    def new_room_player(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['content'],
        })
