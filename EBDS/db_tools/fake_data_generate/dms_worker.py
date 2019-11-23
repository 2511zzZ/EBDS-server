# coding: utf-8
import random
from decimal import Decimal
from EBDS.db_tools.fake_data_generate.tools import date_range
from EBDS.db_tools.fake_data_generate.tools import get_db_connector

# 打开数据库连接
db = get_db_connector()
cursor = db.cursor()
random.seed(12345)


def insert_to_mysql(table_name, begin_date, end_date):
    employee_sql = "SELECT employee_id FROM sms_member WHERE type=1;"
    cursor.execute(employee_sql)
    employee_data = cursor.fetchall()
    # 每个工位的标准
    stat_standard_sql = "SELECT m.stat_id, t.s_efficiency, t.s_accuracy, t.s_workhour FROM standard_team AS t " \
                        "JOIN sms_team_stat_member AS m ON t.team_id=m.team_id;"
    cursor.execute(stat_standard_sql)
    stat_standard_data = cursor.fetchall()

    print(len(employee_data))
    print(len(stat_standard_data))
    for _date in date_range(begin_date, end_date):
        # print(_date)
        flag = 0
        for i in range(0, len(employee_data)):
            if i % 3 == 0:
                # print(flag)
                data = stat_standard_data[flag]
                s_efficiency = data[1]
                s_accuracy = data[2]
                s_workhour = data[3]

                if flag < len(stat_standard_data)-1:
                    flag += 1
            else:
                data = stat_standard_data[flag]
                s_efficiency = data[1]
                s_accuracy = data[2]
                s_workhour = data[3]
            employee_id = employee_data[i][0]
            # print(employee_id, s_efficiency, s_accuracy, s_workhour, flag)
            efficiency = random.choice(
                list(range(int(s_efficiency - Decimal(30.0)), int(s_efficiency))))
            accuracy = random.choice(list(range(int(s_accuracy - Decimal(30.0)), int(s_accuracy))))
            workhour = random.randint(5, int(s_workhour))
            time = _date
            try:
                sql = "INSERT INTO {}(worker_id, efficiency, accuracy, workhour, time) " \
                      "VALUE(%s, %s, %s, %s, %s)".format(table_name)
                val = (employee_id, efficiency, accuracy, workhour, time)
                cursor.execute(sql, val)
                # db.commit()
            except Exception as e:
                # 回滚
                print(e)
                db.rollback()
    db.commit()


def run():
    try:
        insert_to_mysql("dms_worker_daily", "2018-10-20", "2019-11-16")
        db.commit()
    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    run()
