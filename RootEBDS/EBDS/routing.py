# coding: utf-8

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from dms.consumers.online_consumer import OnlineDataConsumer
from ams.consumers.alert_consumer import AlertConsumer
from core.authentication import JsonTokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    'websocket': JsonTokenAuthMiddlewareStack(
        URLRouter([
            path(r'ws/online_data/', OnlineDataConsumer),
            path(r'ws/alert/', AlertConsumer),
        ])
    ),
    # 'websocket': URLRouter([
    #     path(r'ws/alert/', AlertConsumer),
    # ])
})
