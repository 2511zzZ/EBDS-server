# coding: utf-8
from db_tools.tools.tools import get_db_connector

# 打开数据库连接
db = get_db_connector()
cursor = db.cursor()


def insert_to_mysql(table_name, start, end, name):
    """
    插入小组/大组/车间表的结构(id name)
    :param table_name:
    :param start:
    :param end:
    :param name:
    :return:
    """
    for index in range(start, end+1):
        try:
            sql = "INSERT INTO {}(id, name) VALUES(%s, %s)".format(table_name)
            val = (index, name+str(index))
            cursor.execute(sql, val)
            # db.commit()
        except Exception as e:
            # 回滚
            print(e)
            db.rollback()
    db.commit()

    # 小组不进行操作
    if name != "小组":
        _insert_employee_to_mysql(table_name, {"大组": 2, "车间": 3}[name])


def _insert_employee_to_mysql(sms_table_name, sms_type):
    """
    插入大组/车间表的管理员工号(employee_id)
    :param sms_table_name:
    :param sms_type:
    :return:
    """
    sms_sql = "SELECT id FROM {};".format(sms_table_name)
    employee_sql = "SELECT employee_id FROM sms_member WHERE type={};".format(sms_type)
    cursor.execute(sms_sql)
    sms_data = cursor.fetchall()
    cursor.execute(employee_sql)
    employee_data = cursor.fetchall()

    for i in range(len(sms_data)):
        group_id, employee_id = sms_data[i][0], employee_data[i][0]
        try:
            sql = "UPDATE {} SET employee_id = %s WHERE id=%s".format(sms_table_name)
            val = (employee_id, group_id)
            cursor.execute(sql, val)
            db.commit()
        except Exception as e:
            # 回滚
            print(e)
            db.rollback()


def insert_to_dpt(sms_table_name):
    """
    插入生产部信息表
    :return:
    """
    employee_sql = "SELECT employee_id FROM sms_member WHERE type=4 ORDER BY employee_id DESC;"
    cursor.execute(employee_sql)
    employee_data = cursor.fetchall()

    employee_id = employee_data[0][0]  # 总经理
    try:
        sql = "INSERT INTO {}(id, name, employee_id) VALUE(%s, %s, %s)".format(sms_table_name)
        val = (1, "生产部", employee_id, )
        cursor.execute(sql, val)
        db.commit()
    except Exception as e:
        # 回滚
        print(e)
        db.rollback()


def run():
    try:
        insert_to_mysql("sms_team", 1, 500, "小组")
        insert_to_mysql("sms_group", 1, 100, "大组")
        insert_to_mysql("sms_workshop", 1, 35, "车间")

        insert_to_dpt("sms_dpt")

    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    run()
