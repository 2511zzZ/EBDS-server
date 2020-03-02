# coding: utf-8

EMPLOYEE_TYPE_CHOICES = (
    (0, "离职"),
    (1, "工人"),
    (2, "大组长"),
    (3, "经理"),
    (4, "总经理")
)

SEX_CHOICES = (
    ("male", "男"),
    ("female", "女")
)

DAY_PERIOD_CHOICES = (
    ("morning", "早"),
    ("middle", "中"),
    ("night", "晚")
)

STANDARD_TYPE_CHOICES = (
    ("worker", "工人"),
    ("stat", "工位"),
    ("team", "小组"),
    ("group", "大组"),
    ("workshop", "车间"),
    ("dpt", "生产部")
)

AVERAGE_TYPE_CHOICES = (
    ("team", "小组"),
    ("group", "大组"),
    ("workshop", "车间"),
    ("dpt", "生产部"),
    ("stat", "工位")
)

ONLINE_TYPE_CHOICES = AVERAGE_TYPE_CHOICES

DAILY_TYPE_CHOICES = STANDARD_TYPE_CHOICES

METRIC_CHOICES = (
    ("efficiency", "效率"),
    ("accuracy", "准确率"),
    ("workhour", "有效工时")
)

FORM_TYPE_CHOICES = (
    ("alert", "警报"),
    ("team", "小组"),
    ("group", "大组"),
    ("workshop", "车间"),
    ("dpt", "生产部"),
    ("stat", "工位"),
    ("worker", "工人")
)

FORM_EXPORT_CHOICES = (
    "excel",
    "pdf"
)

# 警报相关
ALERT_ROLE_CHOICES = (
    (2, "大组长"),
    (3, "经理"),
    (4, "总经理")
)

ALERT_STATUS = (
    (-1, "异常警报"),  # 系统关闭重启时可能会出现
    (1, "待处理"),
    (2, "已处理"),
    (3, "已关闭")
)

ALERT_STATUS_FOR_FILTER = (
    (1, "待处理"),
    (2, "已处理"),
    (3, "已关闭/异常警报")  # 对应status为3/-1
)

ALERT_REASON = (
    "持续{}分钟{}未达标",  # 比如 持续10分钟效率未达标
    "缺人持续{}分钟"
)
