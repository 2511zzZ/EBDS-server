# coding: utf-8
import datetime
import subprocess

import mysql.connector
from EBDS.db_tools.data.dbconfig import CONFIG


def date_range(begin, end):
    dates = []
    dt = datetime.datetime.strptime(begin, "%Y-%m-%d")
    date = begin[:]
    while date <= end:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates


def get_db_connector():
    return mysql.connector.connect(
        host=CONFIG["HOST"],
        user=CONFIG["USER"],
        passwd=CONFIG["PASSWD"],  # 写上你的数据库密码
        database=CONFIG["DATABASE"],
        auth_plugin='mysql_native_password'
    )


def exec_sql_file(path: str):
    # 这里不使用python去读sql,因为python的mysql客户端无法判断整个文件中sql语句的执行逻辑
    cmd = ["mysql", "-h", CONFIG["HOST"], "-u", CONFIG["USER"], CONFIG["DATABASE"]]  # "-p%s" % CONFIG["PASSWD"],
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output = process.communicate(("source " + path).encode())
    return output[1] is None


if __name__ == '__main__':
    exec_sql_file("/Users/mac/PycharmProjects/EBDS-server/procedure.sql")

