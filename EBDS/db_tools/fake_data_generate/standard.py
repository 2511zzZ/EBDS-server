# coding: utf-8
import random
from EBDS.db_tools.fake_data_generate.tools import get_db_connector

# 打开数据库连接
db = get_db_connector()
cursor = db.cursor()
random.seed(12345)


def insert_to_mysql(table_name):
    sms_sql = "SELECT id FROM sms_{};".format(table_name.split("_")[-1])
    cursor.execute(sms_sql)
    sms_data = cursor.fetchall()

    # print(len(sms_data))
    for team_id in range(1, len(sms_data)+1):
        s_efficiency = random.randint(60, 95)
        s_accuracy = random.randint(70, 100)
        s_workhour = random.randint(15, 60)

        # print(team_id, s_efficiency, s_accuracy, s_workhour)
        try:
            sql = "INSERT INTO {}({}_id, s_efficiency, s_accuracy, s_workhour) " \
                  "VALUES(%s, %s, %s, %s);".format(table_name, table_name.split("_")[-1])
            val = (team_id, s_efficiency, s_accuracy, s_workhour)
            cursor.execute(sql, val)
            # db.commit()
        except Exception as e:
            # 回滚
            print(e)
            db.rollback()
    db.commit()


def insert_standard_dpt(table_name):
    """
    插入生产部标准指标表
    :param table_name:
    :return:
    """
    s_efficiency = random.randint(60, 95)
    s_accuracy = random.randint(70, 100)
    s_workhour = random.randint(15, 60)

    # print(team_id, s_efficiency, s_accuracy, s_workhour)
    try:
        sql = "INSERT INTO {}(s_efficiency, s_accuracy, s_workhour) " \
              "VALUES(%s, %s, %s);".format(table_name)
        val = (s_efficiency, s_accuracy, s_workhour)
        cursor.execute(sql, val)
        db.commit()
    except Exception as e:
        # 回滚
        print(e)
        db.rollback()


def run():
    try:
        insert_to_mysql("standard_team")
        insert_to_mysql("standard_group")
        insert_to_mysql("standard_workshop")

        insert_standard_dpt("standard_dpt")

    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    run()
