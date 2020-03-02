# coding: utf-8
import os
import asyncio
import json
from collections import namedtuple
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from utils.person_permissions import OnlinePermission
from django.contrib.auth import get_user_model
from utils.redis_tools import RedisClient

User = get_user_model()


class OnlineDataConsumer(AsyncJsonWebsocketConsumer):
    # 模拟restframework的Request,使得restframework的权限管理在ws得以复用
    SimpleRequest = namedtuple('SimpleRequest', ['user', 'query_params'])
    user_req_dict = {}  # 保存用户与当前所在页的字典

    def __init__(self, scope):
        super(OnlineDataConsumer, self).__init__(scope)
        self.user = None
        self.user_name = None
        self.permission_class = OnlinePermission

        self.request = None  # SimpleRequest的实例
        self.permission_func = self.permission_class().has_permission  # 鉴权的方法

        # 把user_req_dict放入redis中 使得celery的worker可以获取
        self.redis = RedisClient().redis

    async def connect(self):
        self.user = self.scope['user']
        self.user_name = self.scope['user'].username
        print(f'>>> {self.user_name} connected WebSocket')
        await self.channel_layer.group_add(self.user_name, self.channel_name)
        # init user_req_dict
        OnlineDataConsumer.user_req_dict[self.user_name] = None
        self.redis.hset('ws', 'ws_online_data', json.dumps(OnlineDataConsumer.user_req_dict))
        await self.accept()

    async def receive_json(self, content, **kwargs):
        """
        content : {"cur_req": {"type": "group", "id": 100, "metric": "accuracy"}}

        :param content:
        :param kwargs:
        :return:
        """
        print(content)
        try:
            for key in ['type', 'id', 'metric']:
                assert key in content.get('cur_req')
            OnlineDataConsumer.user_req_dict[self.user_name] = content.get('cur_req')
            self.redis.hset('ws', 'ws_online_data', json.dumps(OnlineDataConsumer.user_req_dict))

            self.request = OnlineDataConsumer.SimpleRequest(self.user, content.get('cur_req'))
        except (KeyError, AssertionError):
            # 重置request实例
            self.request = None
            await self.send_json({"error": "请求格式错误"})
            return
        else:
            # 权限管理
            has_permisson = await self.has_permission()
            if not has_permisson:
                OnlineDataConsumer.user_req_dict[self.user_name] = None
                self.redis.hset('ws', 'ws_online_data', json.dumps(OnlineDataConsumer.user_req_dict))
                await self.send_json({"error": "没有权限"})
                return

        await self.send_json(["ok"])

    async def disconnect(self, close_code):
        # 关闭channel时候处理
        del OnlineDataConsumer.user_req_dict[self.user_name]
        self.redis.hset('ws', 'ws_online_data', json.dumps(OnlineDataConsumer.user_req_dict))
        await self.channel_layer.group_discard(
            self.user_name,
            self.channel_name
        )

    async def online_message(self, event):
        # Handles the "online.message" event when it's sent to us.
        print(event)
        if event["content"] != OnlineDataConsumer.user_req_dict[event["username"]]:
            return
        await self.send_json({
            "message": event["message"],
        })

    @database_sync_to_async
    def has_permission(self):
        if self.request:
            return self.permission_func(self.request, None)
        return False

