import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
from apps.extra_tasks.configs import SEND_ITERVAL, BACKEND_URL, BROKER_URL


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EBDS.settings')  # 设置django环境

app = Celery('EBDS', broker=BROKER_URL, backend=BACKEND_URL, include=['extra_tasks.tasks', 'extra_tasks.run'])
app.config_from_object('django.conf:settings', namespace='CELERY')      # 使用CELERY_ 作为前缀，在settings中写配置
app.autodiscover_tasks()  # 发现任务文件每个app下的task.py

INTO_DAILY_TIME = {"hour": 0, "minute": 0}      # daily表的插入时间(每天)

app.conf.beat_schedule = {
    'start_tasks': {
        # 执行into_stat_daily函数
        'task': 'extra_tasks.run.start',
        # 每分钟执行
        'schedule': timedelta(seconds=SEND_ITERVAL),
        # 传递参数
        'args': None,
    },
    'into_stat_daily': {
        # 执行into_stat_daily函数
        'task': 'extra_tasks.tasks.into_daily_task',
        # 每天午夜(0点0分)执行
        'schedule': crontab(minute=INTO_DAILY_TIME["minute"], hour=INTO_DAILY_TIME["hour"]),
        # 传递参数
        'args': None,
    },
    'into_worker_daily': {
        # 执行into_worker_daily_task函数
        'task': 'extra_tasks.tasks.into_worker_daily_task',
        # 每天午夜(0点0分)执行
        'schedule': crontab(minute=INTO_DAILY_TIME["minute"], hour=INTO_DAILY_TIME["hour"]),
        # 传递参数
        'args': None,
    },
}