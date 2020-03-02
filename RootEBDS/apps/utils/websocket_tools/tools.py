# coding: utf-8
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class WSOnline:
    @staticmethod
    def send_message(user, content, message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(user, {"type": "online.message",
                                                       'username': user,
                                                       'content': content,
                                                       'message': message})


class WSAlert:
    @staticmethod
    def send_message(user):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(user, {"type": "alert.message"})

