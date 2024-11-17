import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"game_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['action'] == 'play_card':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_game_state',
                    'player': data['player'],
                    'card': data['card']
                }
            )

    async def update_game_state(self, event):
        await self.send(text_data=json.dumps({
            'player': event['player'],
            'card': event['card']
        }))