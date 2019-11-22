# coding: utf-8
import os
import random
from decimal import Decimal
from EBDS.db_tools.fake_data_generate.tools import date_range
from EBDS.db_tools.fake_data_generate.tools import get_db_connector

# 打开数据库连接
db = get_db_connector()
cursor = db.cursor()
random.seed(12345)

# 打开数据库连接


def insert_to_mysql(table_name, begin_date, end_date):
    # 每个工位的标准
    stat_standard_sql = "SELECT m.stat_id, t.s_efficiency, t.s_accuracy, t.s_workhour FROM standard_team AS t " \
                        "JOIN sms_team_stat_member AS m ON t.team_id=m.team_id;"
    cursor.execute(stat_standard_sql)
    stat_standard_data = cursor.fetchall()
    for _date in date_range(begin_date, end_date):
        # print(_date)
        for data in stat_standard_data:
            stat_id = data[0]
            standard_efficiency = data[1]
            standard_accuracy = data[2]
            standard_workhour = data[3]

            efficiency = random.choice([Decimal(0)]+list(range(int(standard_efficiency-Decimal(30.0)), int(standard_efficiency))))
            accuracy = random.choice([0]+list(range(int(standard_accuracy-Decimal(30.0)), int(standard_accuracy))))
            workhour = random.randint(0, int(standard_workhour))
            time = _date

            try:
                sql = "INSERT INTO {}(stat_id, efficiency, accuracy, workhour, time) VALUES(%s, %s, %s, %s, %s)".format(table_name)
                val = (stat_id, efficiency, accuracy, workhour, time)
                cursor.execute(sql, val)
                # db.commit()
            except Exception as e:
                # 回滚
                print(e)
                db.rollback()
    db.commit()


def run():
    try:
        insert_to_mysql("dms_stat_daily", "2018-10-20", "2019-11-16")

        cursor.callproc('fake_dms_stat_online', ('2019-11-21 00:00:00', 1440))  # 插入全天的数据
        db.commit()
        cursor.callproc('fake_dms_stat_avg')
        db.commit()
    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    # for _date in date_range("2019-10-01", "2019-12-03"):
    #     print(_date)
    run()


