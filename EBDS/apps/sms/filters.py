# coding: utf-8

import django_filters
from django.db.models import Q

from .models import TeamGroupWorkshop, TeamStatMember, Member


class TeamFilter(django_filters.rest_framework.FilterSet):
    team = django_filters.NumberFilter(field_name='team', help_text="小组号", lookup_expr='exact')

    team_name = django_filters.CharFilter(field_name='team__name',  # 跨关系查询
                                          help_text='小组名', lookup_expr='icontains')

    group = django_filters.NumberFilter(field_name='group', help_text="所属大组号", lookup_expr='exact')
    
    workshop = django_filters.NumberFilter(field_name='workshop', help_text="所属车间号", lookup_expr='exact')

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

    workshop = django_filters.NumberFilter(field_name='workshop', help_text="所属车间号", lookup_expr='exact')

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


class StatFilter(django_filters.rest_framework.FilterSet):
    stat = django_filters.NumberFilter(field_name='stat_id', help_text='工位号', lookup_expr='exact')

    morning_shift_id = django_filters.NumberFilter(field_name='morning_shift_id',
                                                   help_text='早班员工号', lookup_expr='exact')

    middle_shift_id = django_filters.NumberFilter(field_name='middle_shift_id',
                                                  help_text='中班员工号', lookup_expr='exact')

    night_shift_id = django_filters.NumberFilter(field_name='night_shift_id',
                                                 help_text='晚班员工号', lookup_expr='exact')

    team = django_filters.NumberFilter(field_name='team',
                                       help_text='所属小组号', lookup_expr='exact')

    team_name = django_filters.CharFilter(field_name='team__name',
                                          help_text='所属小组名字', lookup_expr='icontains')

    shift_name = django_filters.CharFilter(method='shift_name_filter', help_text='员工姓名')

    def shift_name_filter(self, queryset, name, value):
        """根据员工姓名筛选"""
        employee_ids = Member.objects.filter(type=1, name__icontains=value).values('employee_id')

        return queryset.filter(
                    Q(morning_shift_id__in=employee_ids) |
                    Q(middle_shift_id__in=employee_ids) |
                    Q(night_shift_id__in=employee_ids)
                )

    class Meta:
        model = TeamStatMember
        fields = ['stat', 'morning_shift_id', 'middle_shift_id',
                  'night_shift_id', 'team', 'team_name', 'shift_name']
