# coding:utf8
STAT_NUMBER = 5000          # 工位数量
WORKER_NUMBER = 15000       # 工人数量
SEND_ITERVAL = 60           # celery产生数据的时间间隔/秒
RESEARCH_INTERVAL = 120      # avg表中断重查的时间阈值/秒
DAILY_UPDATE_ITERVAL = 5 * 60                                   # daily表查询时间范围/秒
DAILY_UPDATE_TIME = {"hour": 0, "minute": 0, "second": 0}       # daily表每天的更新时间/时分秒
DAILY_RETRY_OPTIONS = {'max_retries': 5, 'countdown': 60}       # daily任务重试选项/重试次数,重试时间间隔

BROKER_URL = 'pyamqp://guest:guest@192.168.99.100//'
BACKEND_URL = 'redis://127.0.0.1:6379'

levels = {"dpt": "workshop",    # 各级别对应的下级name
          "workshop": "group",
          "group": "team",
          "team": "stat"}




