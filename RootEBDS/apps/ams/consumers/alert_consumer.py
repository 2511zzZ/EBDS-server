# coding: utf-8
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class AlertConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user_name = self.scope['user'].username
        print(f'>>> {user_name} connected AlertWebSocket')
        await self.channel_layer.group_add(user_name, self.channel_name)
        await self.accept()

    async def receive_json(self, content, **kwargs):
        pass

    async def disconnect(self, close_code):
        # 关闭channel时候处理
        await self.channel_layer.group_discard(
            self.scope['user'].username,
            self.channel_name
        )

    async def alert_message(self, event):
        # Handles the "alert.message" event when it's sent to us.
        print("已经发送了")
        await self.send_json({
            "message": "",   # 发送空字符串让前端去请求接口进行更新
        })


