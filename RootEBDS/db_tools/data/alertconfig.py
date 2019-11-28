# coding: utf-8

# 警报条件参数
ALERT_CONDITION = {
    "duration": 10,  # 10 min
    "percent": 0.25     # 25%
}

# 警报传递参数
ALERT_TRANSFER = {
    "timeout": 30,  # one hour
    "max_timeout": 720  # one day
}

# 工作时间段
WORK_PERIOD = {
    "morning": ["00:00:00", "07:59:59"],
    "middle": ["08:00:00", "15:59:59"],
    "night": ["16:00:00", "23:59:59"]
}

