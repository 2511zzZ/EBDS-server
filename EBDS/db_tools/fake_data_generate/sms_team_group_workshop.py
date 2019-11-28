# coding: utf-8
from EBDS.db_tools.tools.tools import get_db_connector

# 打开数据库连接
db = get_db_connector()
cursor = db.cursor()


def insert_to_mysql(table_name):
    team_sql = "SELECT id FROM sms_team;"
    group_sql = "SELECT id FROM sms_group;"
    workshop_sql = "SELECT id FROM sms_workshop;"
    cursor.execute(team_sql)
    team_data = cursor.fetchall()
    cursor.execute(group_sql)
    group_data = cursor.fetchall()
    cursor.execute(workshop_sql)
    workshop_data = cursor.fetchall()

    # print(len(team_data))
    # print(len(group_data))
    # print(len(workshop_data))
    for i in range(1, len(team_data)+1):
        group_id = ((i-1) // 5)+1
        if group_id <= 90:
            workshop_id = (group_id-1) // 3 + 1
        else:
            workshop_id = 90/3 + (group_id-1-90) // 2 + 1

        # print(i, group_id, workshop_id)
        try:
            sql = "INSERT INTO {}(team_id, group_id, workshop_id) VALUES(%s, %s, %s)".format(table_name)
            val = (i, group_id, workshop_id)
            cursor.execute(sql, val)
            db.commit()
        except Exception as e:
            # 回滚
            print(e)
            db.rollback()


def run():
    try:
        insert_to_mysql("sms_team_group_workshop")
    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    run()





