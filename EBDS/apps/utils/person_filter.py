# coding: utf-8
"""
自定义的django-filter字段和基类
"""
import django_filters
from rest_framework import filters
from sms.models import Group, Workshop
from django.db.models import Min


class ListFilter(django_filters.CharFilter):
    """
    根据分隔符可传递多个值的字段
    """
    def filter(self, qs, value):
        value = list(filter(None, value.split(",")))
        return super().filter(qs=qs, value=value)


class TeamGroupWorkshopFilterBackend(filters.BaseFilterBackend):
    """
    过滤每个用户所管理的team/group/workshop数据
    """
    def filter_queryset(self, request, queryset, view):
        user = request.user
        role_id = user.groups.all()[0].id
        group_by_keyword = view.ordering[0]
        if role_id == 4:
            # 单字段去重后并获得每个group的第一条queryset
            # 等价于:
            # SELECT * FROM sms_team_group_workshop WHERE team_id in
            # (SELECT MIN(team_id) FROM sms_team_group_workshop GROUP BY workshop_id);
            return queryset.filter(team__in=
                                   queryset.values(group_by_keyword).
                                   annotate(team_id=Min('team')).
                                   values('team_id')
                                   )
        elif role_id == 3:
            _id = Workshop.objects.get(employee=user.employee_id).id  # 获得经理管理车间号
            return queryset.filter(workshop=_id).filter(team__in=
                                                        queryset.values(group_by_keyword).
                                                        annotate(team_id=Min('team')).
                                                        values('team_id')
                                                        )
        elif role_id == 2:
            _id = Group.objects.get(employee=user.employee_id).id  # 获得大组长管理大组号
            return queryset.filter(group=_id).filter(team__in=
                                                     queryset.values(group_by_keyword).
                                                     annotate(team_id=Min('team')).
                                                     values('team_id')
                                                     )
