# coding: utf-8
from sms.models import TeamStatMember
from django.db.models import Max, Q


def get_recent_stat_obj(team_id):
    """
    根据小组号获取小组对应的最新十个工位信息
    :return:
    """
    for stat_obj in TeamStatMember.objects.filter(
                                            id__in=
                                            TeamStatMember.objects.values('stat_id').
                                            annotate(default_id=Max('id')).
                                            values('default_id')
                                            ).filter(team=team_id):
        yield stat_obj


def get_recent_employee_stat_obj(employee_id):
    """
    返回员工目前所在的工位
    :return:
    """
    return TeamStatMember.objects.filter(
        Q(morning_shift_id=employee_id) |
        Q(middle_shift_id=employee_id) |
        Q(night_shift_id=employee_id)
    ).order_by('-update_time')[0]
