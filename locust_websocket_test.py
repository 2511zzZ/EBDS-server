# coding: utf-8
"""
在测试前把websocket的路由权限认证放开(routing.py)
pip install websocket-client-py3, locust
启动命令：locust -f locust_websocket_test.py --host=http://127.0.0.1:8001
"""
import gzip
import json
import time

import websocket
from locust import TaskSet, events, Locust, task


class WebSocketClient(object):
    def connect(self, url):
        try:
            self.ws = websocket.WebSocketApp(url)
            self.ws.on_message = self.on_message
            self.ws.on_error = self.on_error
            self.ws.on_close = self.on_close
        except websocket.WebSocketTimeoutException as e:
            events.request_failure.fire(request_type="web_socket", name='ws', response_time=time.time(), exception=e)
        else:
            events.request_success.fire(request_type="web_socket", name='ws', response_time=time.time(),
                                        response_length=0)
        return self.ws

    def on_message(self, message):
        pass

    def on_error(self, error):
        print('!!! error !!!', error)

    def on_close(self):
        print("### closed ###")

    def on_open(self, obj):
        print('opened')


class WebSocketLocust(Locust):
    def __init__(self):
        super(WebSocketLocust, self).__init__()
        self.client = WebSocketClient()


class UserBehavior(TaskSet):
    def on_start(self):
        print('--------- task start ------------')
        self.url = 'ws://127.0.0.1:8001/ws/alert/'

    def on_stop(self):
        print('---------- task stop ------------')

    @task
    def test_ws(self):
        ws = self.client.connect(self.url)
        ws.run_forever()


class WebsiteUser(WebSocketLocust):
    task_set = UserBehavior
    # 每次执行任务后等待的时间范围(单位秒)
    min_wait = 5000
    max_wait = 9000
