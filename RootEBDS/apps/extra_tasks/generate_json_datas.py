import random
import datetime

from db_tools.tools.tools import get_db_connector
from apps.extra_tasks.configs import STAT_NUMBER, levels


def get_structure(level: str):
    """
    :param level: 要查询的结构的级别
    :return: 该级别对应下级的结构 structure:dict, 级别名称level: str
    """
    structure = dict()
    connection = get_db_connector()
    cursor = connection.cursor()
    if level is "team":
        cursor.execute("SELECT team_id FROM sms_team_stat_member GROUP BY team_id")
        team_id_list = [i[0] for i in cursor.fetchall()]
        for team_id in team_id_list:
            cursor.execute("SELECT stat_id FROM sms_team_stat_member WHERE team_id = {}".format(team_id))
            structure[team_id] = [i[0] for i in cursor.fetchall()]
    elif level in ["group", "workshop"]:
        cursor = connection.cursor()
        cursor.execute("SELECT {} FROM sms_team_group_workshop GROUP BY {}".format(level+"_id", level+"_id"))
        group_id_list = [i[0] for i in cursor.fetchall()]
        for group_id in group_id_list:
            cursor.execute("SELECT {} FROM sms_team_group_workshop WHERE {} = {} GROUP BY {}"
                           .format(levels[level]+"_id", level+"_id", group_id, levels[level]+"_id"))
            structure[group_id] = [i[0] for i in cursor.fetchall()]
    elif level is "dpt":
        cursor.execute("SELECT workshop_id FROM sms_team_group_workshop GROUP BY workshop_id")
        workshop_list = [i[0] for i in cursor.fetchall()]
        structure[1] = workshop_list
    else:
        # raise Exception
        return None
    cursor.close()
    connection.close()
    return structure, level


def random_json(stat_number=STAT_NUMBER):
    print("random_json ing...")
    json_data = list()
    datetime_now = datetime.datetime.now()
    for stat_id in range(1, stat_number+1):
        stat_data = dict()
        stat_data["efficiency"] = round((random.random() * 100), 1)
        stat_data["accuracy"] = round((random.random() * 100), 1)
        stat_data["workhour"] = round((random.random() * 100), 1)
        stat_data["time"] = datetime_now
        stat_data["stat_id"] = stat_id
        json_data.append(stat_data)
    return json_data


def get_superior_data(json_data_list: list, structure: dict):
    """
    :param json_data_list: 下级结构的json数据
    :param structure: 上下级的结构
    :return: 上级的json数据
    """
    superior_data_list = list()
    for superior_id in structure[0].keys():
        superior_data = dict()
        superior_data["efficiency"] = 0
        superior_data["accuracy"] = 0
        superior_data["workhour"] = 0
        superior_data[structure[1]+"_id"] = superior_id
        superior_data["time"] = json_data_list[0]["time"]
        for json_data in json_data_list:
            if json_data[levels[structure[1]]+"_id"] in structure[0][superior_id]:
                for key in ["efficiency", "accuracy", "workhour"]:
                    superior_data[key] += json_data[key]/len(structure[0][superior_id])
                for key in ["efficiency", "accuracy", "workhour"]:
                    superior_data[key] = round(superior_data[key], 1)

        superior_data_list.append(superior_data)
    return superior_data_list





