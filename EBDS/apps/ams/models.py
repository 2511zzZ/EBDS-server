from django.db import models


class AmsBaseInfo(models.Model):
    """
    警报基本信息
    """
    ROLE_CHOICES = (
        (1, "大组长"),
        (2, "经理"),
        (3, "总经理")
    )

    STATUS = (
        (1, "待处理"),
        (2, "已处理"),
        (3, "已关闭")
    )

    alert_id = models.BigIntegerField(verbose_name='警报号', primary_key=True)
    stat_id = models.IntegerField(verbose_name='工位号', blank=True, null=True)
    # 因为警报信息具有历史性，这里不设置外键
    employee_id = models.IntegerField(verbose_name='工位对应员工号', blank=True, null=True)
    employee_name = models.CharField(verbose_name='员工姓名', max_length=255, blank=True, null=True)
    reason = models.CharField(verbose_name='警报原因', max_length=255, blank=True, null=True)
    start_time = models.DateTimeField(verbose_name='开始时间', blank=True, null=True)
    end_time = models.DateTimeField(verbose_name='结束时间', blank=True, null=True)
    final_deal_employee_id = models.IntegerField(verbose_name='最终处理人员工号', blank=True, null=True)
    final_deal_employee_name = models.CharField(verbose_name='最终处理人姓名', max_length=255, blank=True, null=True)
    deal_role_id = models.IntegerField(verbose_name='最终处理人角色类别', blank=True, null=True, choices=ROLE_CHOICES)
    status = models.IntegerField(verbose_name='警报状态', blank=True, null=True, choices=STATUS)

    class Meta:
        db_table = 'ams_base_info'
        verbose_name = "警报基本信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.alert_id)


class AmsConveyInfo(models.Model):
    """
    警报传递信息
    """
    ROLE_CHOICES = (
        (1, "大组长"),
        (2, "经理"),
        (3, "总经理")
    )

    alert = models.ForeignKey(AmsBaseInfo, verbose_name='警报号', related_name='alert_convey_info',
                              on_delete=models.CASCADE, db_constraint=False)
    # 因为警报信息具有历史性，这里不设置外键
    deal_employee_id = models.IntegerField(verbose_name='处理人员工号', blank=True, null=True)
    deal_employee_name = models.CharField(verbose_name='处理人姓名', max_length=255, blank=True, null=True)
    role_id = models.IntegerField(verbose_name='处理人角色类别', blank=True, null=True, choices=ROLE_CHOICES)
    is_timeout = models.BooleanField(default=False, verbose_name='是否超时', blank=True, null=True)
    is_delete = models.BooleanField(default=False, verbose_name='是否删除', blank=True, null=True)
    time = models.DateTimeField(verbose_name='收到警报的时间', blank=True, null=True)

    class Meta:
        db_table = 'ams_convey_info'
        verbose_name = "警报传递信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.alert_id)

