from django.db import models
from sms.models import Team, Group, Workshop


class Standard(models.Model):
    """
    标准指标抽象类
    """
    s_efficiency = models.DecimalField(verbose_name='标准效率', max_digits=6, decimal_places=1, blank=True, null=True)
    s_accuracy = models.DecimalField(verbose_name='标准准确率', max_digits=6, decimal_places=1, blank=True, null=True)
    s_workhour = models.DecimalField(verbose_name='标准有效工时', max_digits=6, decimal_places=1, blank=True, null=True)

    class Meta:
        abstract = True


class StandardTeam(Standard):
    """
    小组标准指标
    """
    team = models.OneToOneField(Team, verbose_name='小组号', related_name='team_standard', primary_key=True,
                                on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = 'standard_team'
        verbose_name = "小组标准指标"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.team.name


class StandardGroup(Standard):
    """
    大组标准指标
    """
    group = models.OneToOneField(Group, verbose_name='大组号', related_name='group_standard', primary_key=True,
                                 on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = 'standard_group'
        verbose_name = "大组标准指标"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group.name


class StandardWorkshop(Standard):
    """
    车间标准指标
    """
    workshop = models.OneToOneField(Workshop, verbose_name='车间号', related_name='workshop_standard', primary_key=True,
                                    on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = 'standard_workshop'
        verbose_name = "车间标准指标"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.workshop.name


class StandardDpt(Standard):
    """
    生产部标准指标
    """

    class Meta:
        db_table = 'standard_dpt'
        verbose_name = "生产部标准指标"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "生产部"


class StandardBasicAction(models.Model):
    """
    基本动作标准
    """
    action_id = models.IntegerField(blank=True, null=True)
    time = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        # TODO：后期完善
        managed = False
        db_table = 'standard_basic_action'




