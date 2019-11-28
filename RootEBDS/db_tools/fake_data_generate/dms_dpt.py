# coding: utf-8
from db_tools.tools.tools import get_db_connector

# 打开数据库连接
db = get_db_connector()
cursor = db.cursor()


def run():
    try:
        cursor.callproc('fake_dms_dpt_daily')
        db.commit()
        cursor.callproc('fake_dms_dpt_online')
        db.commit()
        cursor.callproc('fake_dms_dpt_avg')
        db.commit()

    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    run()


