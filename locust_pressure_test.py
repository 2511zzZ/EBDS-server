# coding: utf-8
"""
对接口进行压力测试
启动命令：locust -f locust_pressure_test.py --host=http://127.0.0.1:8001
"""
import random
from locust import HttpLocust, TaskSet, task, between


class MyTaskSet(TaskSet):
    @task(1)
    def my_task(self):
        header = {"User-Agent": "Mozilla/5.0 "
                                "(Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                                "(KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"}
        self.client.get("online_data/?type=stat&id={}&metric=efficiency".format(
                        random.randint(1, 500)),
                        headers=header)


class User(HttpLocust):
    task_set = MyTaskSet
    wait_time = between(5, 15)
