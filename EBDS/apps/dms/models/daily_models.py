# coding: utf-8
import datetime
from django.db import models


class DailyModel(models.Model):
    """
    每日工作数据抽象类
    """
    efficiency = models.DecimalField(verbose_name='每日效率', max_digits=6, decimal_places=1, blank=True, null=True)
    accuracy = models.DecimalField(verbose_name='每日准确率', max_digits=6, decimal_places=1, blank=True, null=True)
    workhour = models.DecimalField(verbose_name='每日有效工时', max_digits=6, decimal_places=1, blank=True, null=True)
    time = models.DateTimeField(default=datetime.date.today, verbose_name='日期', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        s = ""  # 获取 *_id
        for obj in dir(self):
            if obj.endswith('_id'):
                s = str(getattr(self, obj))
        return s + " {}:".format(self.time) + "-".join(map(str, [self.efficiency, self.accuracy, self.workhour]))


class DmsTeamDaily(DailyModel):
    """
    小组历史工作记录(每日)
    """
    # 历史记录具有历史性，不做外键约束
    team_id = models.IntegerField(verbose_name='小组号')

    class Meta:
        db_table = 'dms_team_daily'
        verbose_name = "小组历史工作记录(每日)"
        verbose_name_plural = verbose_name


class DmsGroupDaily(DailyModel):
    """
    大组历史工作记录(每日)
    """
    group_id = models.IntegerField(verbose_name='大组号')

    class Meta:
        db_table = 'dms_group_daily'
        verbose_name = "大组历史工作记录(每日)"
        verbose_name_plural = verbose_name


class DmsWorkshopDaily(DailyModel):
    """
    车间历史工作记录(每日)
    """
    workshop_id = models.IntegerField(verbose_name='车间号')

    class Meta:
        db_table = 'dms_workshop_daily'
        verbose_name = "车间历史工作记录(每日)"
        verbose_name_plural = verbose_name


class DmsDptDaily(DailyModel):
    """
    生产部历史工作记录(每日)
    """

    class Meta:
        db_table = 'dms_dpt_daily'
        verbose_name = "生产部历史工作记录(每日)"
        verbose_name_plural = verbose_name


class DmsStatDaily(DailyModel):
    """
    工位历史工作记录(每日)
    """
    stat_id = models.IntegerField(verbose_name='工位号')

    class Meta:
        db_table = 'dms_stat_daily'
        verbose_name = "工位历史工作记录(每日)"
        verbose_name_plural = verbose_name


class DmsWorkerDaily(DailyModel):
    """
    工人历史工作记录(每日)
    """
    employee_id = models.IntegerField(verbose_name='员工号')

    class Meta:
        db_table = 'dms_worker_daily'
        verbose_name = "工人历史工作记录(每日)"
        verbose_name_plural = verbose_name


