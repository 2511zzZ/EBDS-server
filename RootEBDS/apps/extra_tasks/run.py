import time
from celery import shared_task

from extra_tasks.configs import STAT_NUMBER
from extra_tasks.tasks import into_online_task, into_avg_task
from extra_tasks.alert_check_task.alert_base_info_method import generate_alert_base_info, convey_alert
from extra_tasks.generate_json_datas import random_json, get_structure, get_superior_data
import json
from .save_datas import SaveData
from utils.redis_tools import RedisClient


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

    generate_alert_base_info()
    convey_alert()

    # 获取redis中的ws_message中的更新数据，并发送到channels
    redis = RedisClient().redis
    try:
        ws_online_send_messages = json.loads(redis.hget('ws', 'ws_online_send_messages'))
    except Exception:
        ws_online_send_messages = None
    SaveData.send_ws_online_message(ws_online_send_messages)
    print(f"ws_online_send_messages发送完成, 共通知{len(ws_online_send_messages) if ws_online_send_messages else 0}条")
    try:
        ws_alert_send_messages = json.loads(redis.hget('ws', 'ws_alert_send_messages'))
    except Exception:
        ws_alert_send_messages = None
    SaveData.send_ws_alert_message(ws_alert_send_messages)
    print(f"ws_online_alert_messages发送完成, 共通知{len(ws_alert_send_messages) if ws_alert_send_messages else 0}条")


@shared_task
def start():
    # 生成各级数据
    stat_data = random_json(STAT_NUMBER)
    team_data = get_superior_data(stat_data, get_structure("team"))
    group_data = get_superior_data(team_data, get_structure("group"))
    workshop_data = get_superior_data(group_data, get_structure("workshop"))
    dpt_data = get_superior_data(workshop_data, get_structure("dpt"))
    start_tasks.delay(stat_data, team_data, group_data, workshop_data, dpt_data)

