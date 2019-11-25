# coding: utf-8

import django_filters
from django.db.models import Q

from .models import TeamGroupWorkshop


class TeamFilter(django_filters.rest_framework.FilterSet):
    team = django_filters.NumberFilter(field_name='team', help_text="小组号", lookup_expr='exact')

    team_name = django_filters.CharFilter(field_name='team__name',  # 跨关系查询
                                          help_text='小组名', lookup_expr='icontains')

    group = django_filters.NumberFilter(field_name='group', help_text="大组号", lookup_expr='exact')
    
    workshop = django_filters.NumberFilter(field_name='workshop', help_text="车间号", lookup_expr='exact')

    class Meta:
        model = TeamGroupWorkshop
        fields = ['team', 'team_name', 'group', 'workshop']


class GroupFilter(django_filters.rest_framework.FilterSet):
    group = django_filters.NumberFilter(field_name='group', help_text="大组号", lookup_expr='exact')

    group_name = django_filters.CharFilter(field_name='group__name',
                                           help_text="大组名", lookup_expr='icontains')

    group_manager = django_filters.NumberFilter(field_name='group__employee',
                                                help_text='大组管理员工号', lookup_expr='exact')

    group_manager_name = django_filters.CharFilter(field_name='group__employee__name',  # 多值跨关系
                                                   help_text='大组管理员姓名', lookup_expr='icontains')

    workshop = django_filters.NumberFilter(field_name='workshop', help_text="车间号", lookup_expr='exact')

    class Meta:
        model = TeamGroupWorkshop
        fields = ['group', 'group_name', 'group_manager', 'group_manager_name', 'workshop']


class WorkshopFilter(django_filters.rest_framework.FilterSet):
    workshop = django_filters.NumberFilter(field_name='workshop', help_text="车间号", lookup_expr='exact')

    workshop_name = django_filters.CharFilter(field_name='workshop__name', help_text="车间名", lookup_expr='icontains')

    workshop_manager = django_filters.NumberFilter(field_name='workshop__employee',
                                                   help_text="车间管理员工号", lookup_expr='exact')

    workshop_manager_name = django_filters.CharFilter(field_name='workshop__employee__name',
                                                      help_text="车间管理员姓名", lookup_expr='icontains')

    class Meta:
        model = TeamGroupWorkshop
        fields = ['workshop', 'workshop_name', 'workshop_manager', 'workshop_manager_name']

