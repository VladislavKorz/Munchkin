import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PlayerAttributeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'room_{self.room_code}'

        # Присоединитесь к группе комнаты
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отсоединитесь от группы комнаты
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        player_id = data['player']
        new_attributes = data['attributes']

        # Обработайте обновление атрибутов и отправьте их обратно всем клиентам
        # Здесь вам нужно будет обновить атрибуты игрока в базе данных
        player = RoomPlayer.objects.get(pk=player_id)
        player_leavel = player.leavel.first()
        player_power = player.power.first()

        player_leavel.leavel = new_attributes['level']
        player_leavel.save()

        player_power.power = new_attributes['power']
        player_power.save()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'update_player_attributes',
                'player_id': player_id,
                'attributes': new_attributes,
            }
        )

    async def update_player_attributes(self, event):
        player_id = event['player_id']
        new_attributes = event['attributes']

        # Отправьте новые атрибуты данному клиенту через WebSocket
        await self.send(text_data=json.dumps({
            'player': player_id,
            'attributes': new_attributes,
        }))
