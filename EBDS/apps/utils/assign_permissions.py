# coding: utf-8
"""
django-guardian assign_perm
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EBDS.EBDS.settings")  # 因为Django工程位于第二级

import django
django.setup()

from users.models import User
from standard.models import StandardTeam, StandardGroup, StandardWorkshop, StandardDpt
from sms.models import Team, Group, Workshop, Dpt, TeamGroupWorkshop
from guardian.shortcuts import assign_perm


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


if __name__ == '__main__':
    assign_standard_perm()





