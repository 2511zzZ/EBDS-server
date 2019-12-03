import datetime

from celery import shared_task
from extra_tasks.into_avg import insert_avg_data
from extra_tasks.into_daily import into_daily, insert_worker_daily_data
from extra_tasks.save_datas import SaveData
from extra_tasks.configs import DAILY_RETRY_OPTIONS


def get_level(jsondata_list):
    for key in jsondata_list[0].keys():
        if key[-2:] == "id":
            return key[:-3]


def into_online_task(jsondata_list):
    table_name = "dms_" + get_level(jsondata_list) + "_online"
    SaveData(jsondata_list, table_name).insert()


def into_avg_task(jsondata_list):
    avg_data_list = insert_avg_data(jsondata_list, get_level(jsondata_list))
    table_name = "dms_"+get_level(jsondata_list)+"_avg"
    if avg_data_list[0] == "insert":
        SaveData(avg_data_list[1], table_name).insert()
    elif avg_data_list[0] == "update":
        SaveData(avg_data_list[1], table_name).update()


@shared_task(autoretry_for=(Exception,), retry_kwargs=DAILY_RETRY_OPTIONS)
def into_daily_task():
    into_daily("stat")
    into_daily("team")
    into_daily("group")
    into_daily("workshop")
    into_daily("dpt")


@shared_task(autoretry_for=(Exception,), retry_kwargs=DAILY_RETRY_OPTIONS)
def into_worker_daily_task():
    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    datetime_now = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
    insert_worker_daily_data(datetime_now)
