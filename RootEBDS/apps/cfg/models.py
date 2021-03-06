from django.db import models
from sms.models import Member
from users.models import User
from core.choices import DAY_PERIOD_CHOICES


class CfgAlertCondition(models.Model):
    """
    警报条件参数
    """
    duration = models.IntegerField(verbose_name='低于标准效率的持续时间(单位:分钟)')
    percent = models.DecimalField(verbose_name='低于标准效率的百分比(小数表示)', max_digits=6, decimal_places=2)

    class Meta:
        db_table = 'cfg_alert_condition'
        verbose_name = "警报条件参数"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "duration={} min,percent={}%".format(self.duration, self.percent*100)


class CfgAlertTransfer(models.Model):
    """
    警报传递参数
    """
    timeout = models.IntegerField(verbose_name='超时传递时间(单位:分钟)')
    max_timeout = models.IntegerField(verbose_name='警报最长处理时间(单位:分钟)')

    class Meta:
        db_table = 'cfg_alert_transfer'
        verbose_name = "警报传递参数"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "timeout={} min,max_timeout={} min".format(self.timeout, self.max_timeout)


class CfgBaseInquiry(models.Model):
    """
    「查询设置」配置
    """
    id = models.IntegerField(verbose_name='配置号', primary_key=True)
    name = models.CharField(verbose_name='配置名', max_length=255, blank=True, null=True)
    mode = models.PositiveSmallIntegerField(verbose_name='使用方式',
                                            help_text=r'如果为1，表示仅使用value, 如果为2表示仅使用status, '
                                                      '如果为3, 表示使用value和status', default=1)
    description = models.CharField(verbose_name='详细描述', max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'cfg_base_inquiry'
        verbose_name = "「查询设置」配置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CfgUserInquiry(models.Model):
    """
    「查询设置」用户配置
    """
    user = models.ForeignKey(User, verbose_name='员工号',
                             on_delete=models.CASCADE, db_constraint=False)
    cfg = models.ForeignKey(CfgBaseInquiry, verbose_name='「查询设置」配置号',
                            on_delete=models.CASCADE, db_constraint=False)
    status = models.BooleanField(default=True, verbose_name='配置开/关', blank=True, null=True)
    value = models.IntegerField(verbose_name='配置值(可选)', blank=True, null=True)

    class Meta:
        db_table = 'cfg_user_inquiry'
        verbose_name = "「查询设置」用户配置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


class CfgWorkPeriod(models.Model):
    """
    工作时间段
    """
    name = models.CharField(max_length=255, verbose_name='时间段', blank=True, null=True, choices=DAY_PERIOD_CHOICES)
    start_time = models.TimeField(verbose_name='开始时间', blank=True, null=True)
    end_time = models.TimeField(verbose_name='结束时间', blank=True, null=True)

    class Meta:
        db_table = 'cfg_work_period'
        verbose_name = "工作时间段"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)
