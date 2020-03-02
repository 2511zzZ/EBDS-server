# coding:utf-8
import time
import os
import json
from django.contrib.auth import get_user_model
from db_tools.tools.tools import get_db_connector
from utils.redis_tools import RedisClient
from utils.websocket_tools.tools import WSOnline, WSAlert
User = get_user_model()


class SaveData:
    def __init__(self, jsondata_list, table_name: str):
        self.connect = get_db_connector()
        self.jsondata_list = jsondata_list
        self.table_name = table_name
        self.level = table_name.split("_")[1]
        self.id_name = self.level+"_id"
        self.redis = RedisClient().redis

    def insert(self):
        # jsondata数据必须按照e, a, w, time, id的顺序排列
        start = time.time()
        ordered_list = list()
        ws_online_send_messages = []   # 需要用websocket推送的信息列表
        for jsondata in self.jsondata_list:
            if self.table_name[-5:] == "daily":     # 插入daily表的数据来源为avg表
                ordered_tuple = (jsondata["a_efficiency"],
                                 jsondata["a_accuracy"],
                                 jsondata["a_workhour"],
                                 jsondata["time"],
                                 jsondata[self.id_name],)
                ordered_list.append(ordered_tuple)
            else:
                ordered_tuple = (jsondata["efficiency"],
                                 jsondata["accuracy"],
                                 jsondata["workhour"],
                                 jsondata["time"],
                                 jsondata[self.id_name],)
                ordered_list.append(ordered_tuple)
                if "online" in self.table_name:
                    self.handle_ws_online_send_message(jsondata, ws_online_send_messages)
                    # HACK:把要发送的信息存到redis中，在avg相关worker完成之后统一发送，
                    # 并在客户端收到online_data时发送avg的http请求(因为online数据更新，avg也会跟着更新)
                    if ws_online_send_messages:  # 有需要发送的消息
                        self.redis.hset('ws', 'ws_online_send_messages', json.dumps(ws_online_send_messages))
        cursor = self.connect.cursor()
        sql = "INSERT INTO {} VALUES (null,%s,%s,%s,%s,%s)".format(self.table_name)
        cursor.executemany(sql, ordered_list)
        self.connect.commit()
        cursor.close()
        print("{}条数据插入{}, 耗时:{}".format(len(self.jsondata_list), self.table_name, time.time()-start))

    def update(self):
        # jsondata数据必须按照e, a, w, time, id的顺序排列
        start = time.time()
        ordered_list = list()
        for jsondata in self.jsondata_list:
            ordered_tuple = (jsondata["efficiency"],
                             jsondata["accuracy"],
                             jsondata["workhour"],
                             jsondata["time"],
                             jsondata[self.id_name],)
            ordered_list.append(ordered_tuple)
        cursor = self.connect.cursor()
        sql = "update {} SET a_efficiency=(%s), a_accuracy=(%s), a_workhour=(%s), time=(%s) where {}=(%s)" \
            .format(self.table_name, self.id_name)
        cursor.executemany(sql, ordered_list)
        self.connect.commit()
        cursor.close()
        print("{}条数据插入{}, 耗时:{}".format(len(self.jsondata_list), self.table_name, time.time() - start))

    def handle_ws_online_send_message(self, jsondata, ws_online_send_messages):
        """
        根据OnlineDataConsumer的当前连接去实时推送数据给相应的用户
        :arg ws_online_send_messages:  需要用websocket推送的信息列表
        """
        try:
            user_req_dict = json.loads(self.redis.hget('ws', 'ws_online_data'))
        except Exception:
            user_req_dict = None
        if user_req_dict:
            for username, req in user_req_dict.items():
                if req \
                        and req["type"] == self.level \
                        and req["id"] == jsondata[self.id_name]:
                    content = {"type": self.level, "id": jsondata[self.id_name], "metric": req["metric"]}
                    message = {self.id_name: jsondata[self.id_name],
                               req["metric"]: {jsondata["time"]: jsondata[req["metric"]]}}
                    ws_online_send_messages.append({'username': username, "content": content, "message": message})

    @staticmethod
    def send_ws_online_message(ws_online_send_messages):
        """发送数据到ws_online"""
        if ws_online_send_messages:
            for online_message in ws_online_send_messages:
                WSOnline.send_message(online_message["username"],
                                      online_message["content"],
                                      online_message["message"])

    @staticmethod
    def send_ws_alert_message(ws_alert_send_messages):
        """发送数据到ws_alert"""
        if ws_alert_send_messages:
            for user in User.objects.filter(employee_id__in=ws_alert_send_messages):
                WSAlert.send_message(user.username)


