# coding: utf-8
import datetime
from django.db import models


class AvgModel(models.Model):
    """
    平均工作数据抽象类(最近)
    """
    a_efficiency = models.DecimalField(verbose_name='平均工作效率', max_digits=6, decimal_places=1, blank=True, null=True)
    a_accuracy = models.DecimalField(verbose_name='平均准确率', max_digits=6, decimal_places=1, blank=True, null=True)
    a_workhour = models.DecimalField(verbose_name='平均有效工时', max_digits=6, decimal_places=1, blank=True, null=True)
    time = models.DateTimeField(default=datetime.datetime.now, verbose_name='时间', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        s = ""  # 获取 *_id
        for obj in dir(self):
            if obj.endswith('_id'):
                s = str(getattr(self, obj))
        return s + " {}:".format(self.time) + "-".join(map(str, [self.a_efficiency, self.a_accuracy, self.a_workhour]))


class DmsTeamAvg(AvgModel):
    """
    小组实时平均工作数据(最近)
    """
    team_id = models.IntegerField(verbose_name='小组号')

    class Meta:
        db_table = 'dms_team_avg'
        verbose_name = "小组实时平均工作数据(最近)"
        verbose_name_plural = verbose_name


class DmsGroupAvg(AvgModel):
    """
    大组实时平均工作数据(最近)
    """
    group_id = models.IntegerField(verbose_name='大组号')

    class Meta:
        db_table = 'dms_group_avg'
        verbose_name = "大组实时平均工作数据(最近)"
        verbose_name_plural = verbose_name


class DmsWorkshopAvg(AvgModel):
    """
    车间实时平均工作数据(最近)
    """
    workshop_id = models.IntegerField(verbose_name='车间号')

    class Meta:
        db_table = 'dms_workshop_avg'
        verbose_name = "车间实时平均工作数据(最近)"
        verbose_name_plural = verbose_name


class DmsDptAvg(AvgModel):
    """
    生产部实时平均工作数据(最近)
    """

    class Meta:
        db_table = 'dms_dpt_avg'
        verbose_name = "生产部实时平均工作数据(最近)"
        verbose_name_plural = verbose_name


class DmsStatAvg(AvgModel):
    """
    工位实时平均工作数据(最近)
    """
    stat_id = models.IntegerField(verbose_name='工位号')

    class Meta:
        db_table = 'dms_stat_avg'
        verbose_name = "工位实时平均工作数据(最近)"
        verbose_name_plural = verbose_name


