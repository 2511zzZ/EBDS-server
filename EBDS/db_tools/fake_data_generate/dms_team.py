# coding: utf-8
from EBDS.db_tools.tools.tools import get_db_connector

# 打开数据库连接
db = get_db_connector()
cursor = db.cursor()


def insert_to_mysql(table_name):
    time_sql = "SELECT DISTINCT time FROM dms_stat_daily;"
    cursor.execute(time_sql)
    time_data = cursor.fetchall()

    for _time in time_data:
        time = _time[0]

        # print(time)
        try:
            sql = "INSERT INTO {}(team_id, efficiency, accuracy, workhour, time) " \
                  "SELECT m.team_id AS team_id, AVG(d.efficiency) AS efficiency, " \
                  "AVG(d.accuracy) AS accuracy, AVG(d.workhour) AS workhour, %s AS time " \
                  "FROM sms_team_stat_member AS m " \
                  "JOIN dms_stat_daily AS d ON m.stat_id = d.stat_id " \
                  "WHERE d.time=DATE(%s) GROUP BY m.team_id;".format(table_name)
            cursor.execute(sql, (time, time))
            # db.commit()
        except Exception as e:
            # 回滚
            print(e)
            db.rollback()
    db.commit()


def run():
    try:
        insert_to_mysql("dms_team_daily")

        cursor.callproc('fake_dms_team_online')
        db.commit()
        cursor.callproc('fake_dms_team_avg')
        db.commit()
    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    run()


