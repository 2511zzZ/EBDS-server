# coding: utf-8
from db_tools.tools.tools import get_db_connector

# 打开数据库连接
db = get_db_connector()
cursor = db.cursor()


def insert_to_mysql(table_name):
    time_sql = "SELECT DISTINCT time FROM dms_group_daily;"
    cursor.execute(time_sql)
    time_data = cursor.fetchall()

    for _time in time_data:
        time = _time[0]

        # print(time)
        try:
            sql = "INSERT INTO {}(workshop_id, efficiency, accuracy, workhour, time) " \
                  "SELECT w.workshop_id AS workshop_id, AVG(d.efficiency) AS efficiency, AVG(d.accuracy) AS accuracy, " \
                  "AVG(d.workhour) AS workhour, %s FROM dms_group_daily AS d " \
                  "JOIN (SELECT DISTINCT(group_id), workshop_id FROM sms_team_group_workshop) AS w ON d.group_id=w.group_id " \
                  "WHERE d.time=DATE(%s) GROUP BY w.workshop_id;".format(table_name)
            cursor.execute(sql, (time, time))
            # db.commit()
        except Exception as e:
            # 回滚
            print(e)
            db.rollback()
    db.commit()


def run():
    try:
        insert_to_mysql("dms_workshop_daily")

        cursor.callproc('fake_dms_workshop_online')
        db.commit()
        cursor.callproc('fake_dms_workshop_avg')
        db.commit()
    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    run()


