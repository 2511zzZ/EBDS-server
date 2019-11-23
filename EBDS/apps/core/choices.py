# coding: utf-8

STANDARD_TYPE_CHOICES = (
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

METRIC_CHOICES = (
    ("efficiency", "效率"),
    ("accuracy", "准确率"),
    ("workhour", "有效工时")
)
