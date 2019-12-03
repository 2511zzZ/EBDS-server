# coding:utf-8
import time

from db_tools.tools.tools import get_db_connector


class SaveData:
    def __init__(self, jsondata_list, table_name: str):
        self.connect = get_db_connector()
        self.jsondata_list = jsondata_list
        self.table_name = table_name
        self.level = table_name.split("_")[1]
        self.id_name = self.level+"_id"

    def insert(self):
        # jsondata数据必须按照e, a, w, time, id的顺序排列
        start = time.time()
        ordered_list = list()
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

