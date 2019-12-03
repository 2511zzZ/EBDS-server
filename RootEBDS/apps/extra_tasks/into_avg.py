import datetime
import decimal
from db_tools.tools.tools import get_db_connector
from extra_tasks.configs import RESEARCH_INTERVAL


def get_avg_fine(one_dict_data, one_old_online_data, one_old_avg_data, old_online_data_num):
    for key in ['efficiency', 'accuracy', 'workhour']:
        one_dict_data[key] = round(((float(one_old_avg_data['a_' + key]) * old_online_data_num
                                     - one_old_online_data[key] + one_dict_data[key])
                                    / old_online_data_num), 1)
    return one_dict_data


def get_avg_no_fine(one_dict_data, one_old_avg_data, old_online_data_num):
    for key in ['efficiency', 'accuracy', 'workhour']:

        one_dict_data[key] = round((float(one_old_avg_data['a_' + key]) * old_online_data_num
                                    + one_dict_data[key])
                                   / (old_online_data_num + 1), 1)
    return one_dict_data


def insert_avg_data(jsondata_list, level):
    connect = get_db_connector()
    cursor = connect.cursor(dictionary=True)
    # 先查询当前avg表的所有数据
    sql = "SELECT * FROM dms_{}_avg".format(level)
    cursor.execute(sql)
    old_avg_data = cursor.fetchall()

    # 当前avg表为空或者有空隔时间段，则重新查表计算平均值插入到avg表
    if len(old_avg_data) == 0:
        cursor.close()
        return "insert", jsondata_list

    # 先查询最后一条avg的time是否与当前时间相差1min以上
    # step2: select avg(*) from dms_{}_online WHERE time >= '{}' and time <= '{}'   # 24小时以内
    # step3: 把重新查表得到的avg值更新到jsondata_list当中
    # 查询距离现在一天时间的所有online数据条数
    cur_time = datetime.datetime.strptime(jsondata_list[0]['time'], "%Y-%m-%dT%H:%M:%S.%f")
    # cur_time = jsondata_list[0]["time"]
    yesterday = cur_time - datetime.timedelta(days=1) - datetime.timedelta(minutes=1)  # 昨天最早实时数据时间
    last_research_time = cur_time - datetime.timedelta(seconds=RESEARCH_INTERVAL)  # 重新查询的最晚时间
    sql = "SELECT count(*) FROM dms_{}_avg WHERE time > '{}'".format(level, last_research_time)
    cursor.execute(sql)
    if not cursor.fetchone()['count(*)']:
        sql = "SELECT AVG(efficiency) as efficiency, AVG(accuracy) as accuracy, AVG(workhour) as workhour, {} as id " \
              "FROM dms_{}_online WHERE time >= '{}' AND time <= '{}' GROUP BY {} ORDER BY id"\
            .format(level+"_id", level, yesterday, cur_time, level+"_id")
        cursor.execute(sql)
        new_avg_data = cursor.fetchall()
        for index, json_data in enumerate(jsondata_list):
            for key in ['efficiency', 'accuracy', 'workhour']:

                json_data[key] = new_avg_data[index+1][key]
        return "update", jsondata_list

    sql = "SELECT count(*) FROM dms_{}_online \
            WHERE time >= '{}' and time <= '{}'".format(level, yesterday, cur_time)
    cursor.execute(sql)
    # 正常情况下num是7,200,000
    num = cursor.fetchone()
    old_online_data_num = num['count(*)'] / len(jsondata_list) - 1


    # 查询距离现在一天时间的最早的online数据
    sql = "SELECT * FROM dms_{}_online \
            WHERE time >= '{}' and time <= '{}' LIMIT 1".format(level, yesterday, cur_time)
    cursor.execute(sql)
    earliest_online_data = cursor.fetchone()
    for i, one_old_avg_data in enumerate(old_avg_data):  # 上次的平均值
        if earliest_online_data['time'] > yesterday:
            jsondata_list[i] = get_avg_no_fine(jsondata_list[i], one_old_avg_data, old_online_data_num)
        else:
            jsondata_list[i] = get_avg_fine(jsondata_list[i], earliest_online_data, one_old_avg_data, old_online_data_num)
    cursor.close()
    return "update", jsondata_list
