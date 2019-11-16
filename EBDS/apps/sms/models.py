from datetime import datetime

from django.db import models


class Member(models.Model):
    """
    公司成员
    """
    TYPE_CHOICES = (
        (0, "工人"),
        (1, "大组长"),
        (2, "经理"),
        (3, "总经理")
    )
    SEX_CHOICES = (
        ("male", "男"),
        ("female", "女")
    )

    employee_id = models.AutoField(verbose_name='员工号', primary_key=True)
    name = models.CharField(verbose_name='姓名', max_length=255, blank=True, null=True)
    sex = models.CharField(verbose_name='性别', max_length=255, blank=True, null=True, choices=SEX_CHOICES)
    birthday = models.DateField(verbose_name='出生日期', blank=True, null=True)
    birthplace = models.CharField(verbose_name='所在地', max_length=255, blank=True, null=True)
    type = models.IntegerField(verbose_name='员工类别', blank=True, null=True, choices=TYPE_CHOICES)

    class Meta:
        db_table = 'sms_member'
        verbose_name = "公司成员"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.employee_id


class Team(models.Model):
    """
    小组结构
    """
    id = models.IntegerField(verbose_name='小组号', primary_key=True)
    name = models.CharField(verbose_name='小组名', max_length=255)

    class Meta:
        db_table = 'sms_team'
        verbose_name = "小组结构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Group(models.Model):
    """
    大组结构
    """
    id = models.IntegerField(verbose_name='大组号', primary_key=True)
    name = models.CharField(verbose_name='大组名', max_length=255)
    employee = models.ForeignKey(Member, verbose_name='大组管理员工号', related_name='employee_group',
                                 on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = 'sms_group'
        verbose_name = "大组结构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Workshop(models.Model):
    """
    车间结构
    """
    id = models.IntegerField(verbose_name='车间号', primary_key=True)
    name = models.CharField(verbose_name='车间名', max_length=255)
    employee = models.ForeignKey(Member, verbose_name='车间管理员工号', related_name='employee_workshop',
                                 on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = 'sms_workshop'
        verbose_name = "车间结构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class TeamGroupWorkshop(models.Model):
    """
    小组-大组-车间层级关系
    """
    team = models.OneToOneField(Team, verbose_name='小组号', related_name='level_relate', primary_key=True,
                                on_delete=models.CASCADE, db_constraint=False)
    group = models.ForeignKey(Group, verbose_name='大组号', related_name='level_relate', on_delete=models.CASCADE, db_constraint=False)
    workshop = models.ForeignKey(Workshop, verbose_name='车间号', related_name='level_relate', on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = 'sms_team_group_workshop'
        verbose_name = "小组-大组-车间层级关系"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "-".join([str(self.team_id), str(self.group_id), str(self.workshop_id)])


class TeamStatMember(models.Model):
    """
    小组工人排班表(包含历史记录)
    """
    team = models.ForeignKey(Team, verbose_name='小组号', related_name='team_stat_member',
                             on_delete=models.CASCADE, db_constraint=False)
    stat_id = models.IntegerField(verbose_name='工位号')
    morning_shift_id = models.IntegerField(verbose_name='早班员工号', blank=True, null=True)
    middle_shift_id = models.IntegerField(verbose_name='中班员工号', blank=True, null=True)
    night_shift_id = models.IntegerField(verbose_name='晚班员工号', blank=True, null=True)
    update_time = models.DateField(verbose_name='记录时间', default=datetime.now, blank=True, null=True)

    class Meta:
        db_table = 'sms_team_stat_member'
        verbose_name = "小组工人排班表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "-".join([str(self.team.name), str(self.stat_id)])




