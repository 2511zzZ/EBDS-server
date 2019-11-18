# coding: utf-8
"""数据库数据生成"""
import os
import sys
from EBDS.db_tools.fake_data_generate.tools import exec_sql_file

BASE_DIR = 'fake_data_generate'
# 定义插入顺序
data_generate_order = ['sms_member', 'auth_user', 'auth_group', 'auth_user_groups',
                       'sms', 'sms_team_group_workshop', 'sms_team_stat_member',
                       'standard', 'dms_stat', 'dms_team', 'dms_group',
                       'dms_workshop', 'dms_dpt', 'dms_worker', 'cfg']
data_generate_order_conf = [BASE_DIR+"."+data_generate_order[index] for index, _ in enumerate(data_generate_order)]


def exec_procedure_sql():
    """导入存储过程到数据库中"""
    db_tools_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(db_tools_path, 'data', 'procedure.sql')
    exec_sql_file(file_path)


def import_data():
    for data_generator in data_generate_order_conf:
        __import__(data_generator)
        moudule = sys.modules[data_generator]
        moudule.run()
        print(getattr(moudule, '__name__'), "导入完成")


if __name__ == '__main__':
    exec_procedure_sql()
    import_data()
