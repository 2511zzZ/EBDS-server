# coding: utf-8
from db_tools.tools.tools import get_db_connector

# 打开数据库连接
db = get_db_connector()
cursor = db.cursor()


def insert_to_mysql(table_name, record_time="2017-10-20"):
    team_sql = "SELECT id FROM sms_team;"
    employee_sql = "SELECT employee_id FROM sms_member WHERE type=1;"
    cursor.execute(team_sql)
    team_data = cursor.fetchall()
    cursor.execute(employee_sql)
    employee_data = cursor.fetchall()

    # print(len(team_data))
    # print(len(employee_data))
    for stat_id in range(1, 5000 + 1):
        team_id = ((stat_id - 1) // 10) + 1
        morning_id, middle_id, night_id = employee_data[3 * stat_id - 3][0], \
                                          employee_data[3 * stat_id - 2][0], employee_data[3 * stat_id - 1][0]
        # print(team_id, stat_id, morning_id, middle_id, night_id)

        try:
            sql = "INSERT INTO {}(team_id, stat_id, morning_shift_id, middle_shift_id, night_shift_id, update_time) " \
                  "VALUES(%s, %s, %s, %s, %s, %s)".format(table_name)
            val = (team_id, stat_id, morning_id, middle_id, night_id, record_time)
            cursor.execute(sql, val)
            # db.commit()
        except Exception as e:
            # 回滚
            print(e)
            db.rollback()
    db.commit()


def run():
    try:
        insert_to_mysql("sms_team_stat_member")
    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    run()

