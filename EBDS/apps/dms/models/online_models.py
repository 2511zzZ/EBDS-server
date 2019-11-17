# coding: utf-8
import datetime
from django.db import models


class OnlineModel(models.Model):
    """
    实时工作数据抽象类
    """
    efficiency = models.DecimalField(verbose_name='实时效率', max_digits=6, decimal_places=1, blank=True, null=True)
    accuracy = models.DecimalField(verbose_name='实时准确率', max_digits=6, decimal_places=1, blank=True, null=True)
    workhour = models.DecimalField(verbose_name='实时有效工时', max_digits=6, decimal_places=1, blank=True, null=True)
    time = models.DateField(default=datetime.datetime.now, verbose_name='时间', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        s = ""  # 获取 *_id
        for obj in dir(self):
            if obj.endswith('_id'):
                s = str(getattr(self, obj))
        return s + " {}:".format(self.time) + "-".join(map(str, [self.efficiency, self.accuracy, self.workhour]))


class DmsTeamOnline(OnlineModel):
    """
    小组实时工作数据(24小时内)
    """
    # 历史记录具有历史性，不做外键约束
    team_id = models.IntegerField(verbose_name='小组号')

    class Meta:
        db_table = 'dms_team_online'
        verbose_name = "小组实时工作数据(24小时内)"
        verbose_name_plural = verbose_name


class DmsGroupOnline(OnlineModel):
    """
    大组实时工作数据(24小时内)
    """
    group_id = models.IntegerField(verbose_name='大组号')

    class Meta:
        db_table = 'dms_group_online'
        verbose_name = "大组实时工作数据(24小时内)"
        verbose_name_plural = verbose_name


class DmsWorkshopOnline(OnlineModel):
    """
    车间实时工作数据(24小时内)
    """
    workshop_id = models.IntegerField(verbose_name='车间号')

    class Meta:
        db_table = 'dms_workshop_online'
        verbose_name = "车间实时工作数据(24小时内)"
        verbose_name_plural = verbose_name


class DmsDptOnline(OnlineModel):
    """
    生产部实时工作数据(24小时内)
    """

    class Meta:
        db_table = 'dms_dpt_online'
        verbose_name = "生产部实时工作数据(24小时内)"
        verbose_name_plural = verbose_name


class DmsStatOnline(OnlineModel):
    """
    工位实时工作数据(24小时内)
    """
    stat_id = models.IntegerField(verbose_name='工位号')

    class Meta:
        db_table = 'dms_stat_online'
        verbose_name = "工位实时工作数据(24小时内)"
        verbose_name_plural = verbose_name


