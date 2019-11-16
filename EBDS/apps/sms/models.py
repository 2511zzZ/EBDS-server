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

    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sex = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    birthplace = models.CharField(max_length=255, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True, choices=TYPE_CHOICES)

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
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

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
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    employee = models.ForeignKey(Member, related_name='employee_group', on_delete=models.CASCADE, db_constraint=False)

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
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    employee = models.ForeignKey(Member, related_name='employee_workshop', on_delete=models.CASCADE, db_constraint=False)

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
    team = models.OneToOneField(Team, related_name='level_relate', primary_key=True, on_delete=models.CASCADE, db_constraint=False)
    group = models.ForeignKey(Group, related_name='level_relate', on_delete=models.CASCADE, db_constraint=False)
    workshop = models.ForeignKey(Workshop, related_name='level_relate', on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        db_table = 'sms_team_group_workshop'
        verbose_name = "小组-大组-车间层级关系"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "-".join([str(self.team_id), str(self.group_id), str(self.workshop_id)])


class TeamStatMember(models.Model):
    """
    小组工人排班
    """
    team = models.ForeignKey(Team, related_name='team_stat_member', on_delete=models.CASCADE, db_constraint=False)
    stat_id = models.IntegerField()
    morning_shift_id = models.IntegerField(blank=True, null=True)
    middle_shift_id = models.IntegerField(blank=True, null=True)
    night_shift_id = models.IntegerField(blank=True, null=True)
    update_time = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'sms_team_stat_member'
        verbose_name = "小组工人排班"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "-".join([str(self.team.name), str(self.stat_id)])




