# coding: utf-8
"""
django-guardian assign_perm
"""

import os

from django.db.models import Max

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RootEBDS.EBDS.settings")  # 因为Django工程位于第二级

import django
django.setup()

from guardian.shortcuts import assign_perm

from users.models import User
from standard.models import StandardTeam, StandardGroup, StandardWorkshop, StandardDpt
from sms.models import Team, Group, Workshop, Dpt, TeamGroupWorkshop, TeamStatMember

from dms.models import DmsStatAvg, DmsTeamAvg, DmsGroupAvg, DmsWorkshopAvg, DmsDptAvg


def assign_standard_perm():
    """
    构建standard的对象级权限
    :return:
    """
    all_sms = ['dpt', 'workshop', 'group', 'team']
    for user in User.objects.all():
        if user.employee_id:
            if user.employee.type == 4:  # 总经理
                for sms_name in all_sms:
                    for standard in globals()['Standard'+sms_name.title()].objects.all():
                        assign_perm(f'view_standard{sms_name}', user, standard)
            elif user.employee.type == 3:  # 经理
                _id = Workshop.objects.get(employee=user.employee_id).id  # 获得经理管理车间号
                for sms_name in all_sms[1:]:
                    # 获得该车间所管辖的小组/大组/车间 字典信息
                    for sms_obj in TeamGroupWorkshop.objects.filter(workshop=_id).values(sms_name).distinct():
                        sms_id = sms_obj[sms_name]
                        standard = globals()['Standard'+sms_name.title()].objects.get(**{sms_name: sms_id})
                        assign_perm(f'view_standard{sms_name}', user, standard)
            elif user.employee.type == 2:  # 大组长
                _id = Group.objects.get(employee=user.employee_id).id  # 获得大组长管理大组号
                for sms_name in all_sms[2:]:
                    # 获得该大组所管辖的小组/大组 字典信息
                    for sms_obj in TeamGroupWorkshop.objects.filter(group=_id).values(sms_name).distinct():
                        sms_id = sms_obj[sms_name]
                        standard = globals()['Standard'+sms_name.title()].objects.get(**{sms_name: sms_id})
                        assign_perm(f'view_standard{sms_name}', user, standard)


def assign_average_perm():
    """
    构建average的对象级权限
    :return:
    """
    all_sms = ['dpt', 'workshop', 'group', 'team', 'stat']
    for user in User.objects.all():
        if user.employee_id:
            if user.employee.type == 4:  # 总经理
                for sms_name in all_sms:
                    for average in globals()[f'Dms{sms_name.title()}Avg'].objects.all():
                        assign_perm(f'view_dms{sms_name}avg', user, average)
            elif user.employee.type == 3:  # 经理
                _id = Workshop.objects.get(employee=user.employee_id).id  # 获得经理管理车间号
                for sms_name in all_sms[1:-1]:
                    # 获得该车间所管辖的小组/大组/车间 字典信息
                    for sms_obj in TeamGroupWorkshop.objects.filter(workshop=_id).values(sms_name).distinct():
                        sms_id = sms_obj[sms_name]
                        average = globals()[f'Dms{sms_name.title()}Avg'].objects.get(**{sms_name+"_id": sms_id})
                        assign_perm(f'view_dms{sms_name}avg', user, average)
                # 获得该车间所管辖的工位 字典信息
                sms_name = all_sms[-1]
                for team_obj in TeamGroupWorkshop.objects.filter(workshop=_id).values('team').distinct():
                    team_id = team_obj['team']
                    # 取小组对应的最新十个工位信息
                    for stat_obj in TeamStatMember.objects.filter(id__in=
                                                                  TeamStatMember.objects.values('stat_id').
                                                                  annotate(default_id=Max('id')).
                                                                  values('default_id')
                                                                  ).filter(team=team_id):
                        stat_id = getattr(stat_obj, f"{sms_name}_id")
                        average = globals()[f'Dms{sms_name.title()}Avg'].objects.get(**{sms_name + "_id": stat_id})
                        assign_perm(f'view_dms{sms_name}avg', user, average)
            # end elif
            elif user.employee.type == 2:  # 大组长
                _id = Group.objects.get(employee=user.employee_id).id  # 获得大组长管理大组号
                for sms_name in all_sms[2:-1]:
                    # 获得该大组所管辖的小组/大组 字典信息
                    for sms_obj in TeamGroupWorkshop.objects.filter(group=_id).values(sms_name).distinct():
                        sms_id = sms_obj[sms_name]
                        average = globals()[f'Dms{sms_name.title()}Avg'].objects.get(**{sms_name + "_id": sms_id})
                        assign_perm(f'view_dms{sms_name}avg', user, average)
                # 获得该大组所管辖的工位 字典信息
                sms_name = all_sms[-1]
                for team_obj in TeamGroupWorkshop.objects.filter(group=_id).values('team').distinct():
                    team_id = team_obj['team']
                    # Solved: 这里存在逻辑上的bug，最近十个并不是最新的工位信息(而应该取每个工位最近的一条记录)
                    for stat_obj in TeamStatMember.objects.filter(id__in=
                                                                  TeamStatMember.objects.values('stat_id').
                                                                  annotate(default_id=Max('id')).
                                                                  values('default_id')
                                                                  ).filter(team=team_id):
                        stat_id = getattr(stat_obj, f"{sms_name}_id")
                        average = globals()[f'Dms{sms_name.title()}Avg'].objects.get(**{sms_name + "_id": stat_id})
                        assign_perm(f'view_dms{sms_name}avg', user, average)
            # end elif


if __name__ == '__main__':
    # assign_standard_perm()
    assign_average_perm()





