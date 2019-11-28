# coding: utf-8
from db_tools.tools.tools import get_db_connector

# 打开数据库连接
db = get_db_connector()
cursor = db.cursor()


def insert_to_mysql(table_name):
    time_sql = "SELECT DISTINCT time FROM dms_team_daily;"
    cursor.execute(time_sql)
    time_data = cursor.fetchall()

    for _time in time_data:
        time = _time[0]

        # print(time)
        try:
            sql = "INSERT INTO {}(group_id, efficiency, accuracy, workhour, time) " \
                  "SELECT w.group_id AS group_id, AVG(d.efficiency) AS efficiency, AVG(d.accuracy) AS accuracy, " \
                  "AVG(d.workhour) AS workhour, %s AS time FROM dms_team_daily AS d " \
                  "JOIN sms_team_group_workshop AS w ON d.team_id=w.team_id " \
                  "WHERE d.time=DATE(%s) GROUP BY w.group_id;".format(table_name)
            cursor.execute(sql, (time, time))
            # db.commit()
        except Exception as e:
            # 回滚
            print(e)
            db.rollback()
    db.commit()


def run():
    insert_to_mysql("dms_group_daily")

    cursor.callproc('fake_dms_group_online')
    db.commit()
    cursor.callproc('fake_dms_group_avg')
    db.commit()


if __name__ == '__main__':
    try:
        run()
    finally:
        cursor.close()
        db.close()


