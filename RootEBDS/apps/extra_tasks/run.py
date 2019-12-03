import time
from celery import shared_task

from extra_tasks.configs import STAT_NUMBER
from extra_tasks.tasks import into_online_task, into_avg_task
from extra_tasks.generate_json_datas import random_json, get_structure, get_superior_data


@shared_task
def start_tasks(stat_data, team_data, group_data, workshop_data, dpt_data):
    # 插入online表
    into_online_task(stat_data)
    into_online_task(team_data)
    into_online_task(group_data)
    into_online_task(workshop_data)
    into_online_task(dpt_data)

    into_avg_task(stat_data)
    into_avg_task(team_data)
    into_avg_task(group_data)
    into_avg_task(workshop_data)
    into_avg_task(dpt_data)


@shared_task
def start():
    # 生成各级数据
    stat_data = random_json(STAT_NUMBER)
    team_data = get_superior_data(stat_data, get_structure("team"))
    group_data = get_superior_data(team_data, get_structure("group"))
    workshop_data = get_superior_data(group_data, get_structure("workshop"))
    dpt_data = get_superior_data(workshop_data, get_structure("dpt"))
    start_tasks.delay(stat_data, team_data, group_data, workshop_data, dpt_data)

