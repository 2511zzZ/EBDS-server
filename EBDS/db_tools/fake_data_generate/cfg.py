# coding: utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EBDS.EBDS.settings")  # 因为Django工程位于第二级

import django
django.setup()

from cfg.models import CfgAlertCondition, CfgAlertTransfer, CfgWorkPeriod
from EBDS.db_tools.data.alertconfig import ALERT_CONDITION, ALERT_TRANSFER, WORK_PERIOD


def insert_to_db():
    # 警报
    CfgAlertCondition.objects.create(duration=ALERT_CONDITION["duration"], percent=ALERT_CONDITION["percent"])
    CfgAlertTransfer.objects.create(timeout=ALERT_TRANSFER["timeout"], max_timeout=ALERT_TRANSFER["max_timeout"])

    # 工作时间段
    for name, time in WORK_PERIOD.items():
        CfgWorkPeriod.objects.create(name=name, start_time=time[0], end_time=time[1])


run = insert_to_db

if __name__ == '__main__':
    insert_to_db()

