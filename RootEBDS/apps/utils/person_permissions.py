# coding: utf-8
from django.db.models import Max
from rest_framework import permissions
from standard.models import StandardTeam, StandardGroup, StandardWorkshop, StandardDpt

from dms.models import DmsTeamAvg, DmsGroupAvg, DmsWorkshopAvg, DmsDptAvg, DmsStatAvg

from dms.models import DmsTeamOnline, DmsGroupOnline, DmsWorkshopOnline, DmsDptOnline, DmsStatOnline

from sms.models import Team, Group, Workshop, Dpt, TeamStatMember, TeamGroupWorkshop

from core.choices import ONLINE_TYPE_CHOICES, DAILY_TYPE_CHOICES
from utils.static_methods import get_recent_stat_obj, get_all_worker_id


class StandardPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    标准指标 对象级权限
    """
    def has_permission(self, request, view):
        sms_name = request.query_params.get('type')
        sms_id = request.query_params.get('id')

        try:
            sms_ids = list(filter(None, sms_id.split(",")))
            # 对象集的权限验证(验证规则all)
            for obj in globals()['Standard' + sms_name.title()].objects.filter(pk__in=sms_ids):
                if not request.user.has_perm(f'view_standard{sms_name}', obj):
                    return False
            return True
        except Exception:  # 出现uncleaned数据交给filter来做处理
            return True

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class AveragePermission(permissions.BasePermission):
    """
    实时平均工作数据 对象级权限
    """
    def has_permission(self, request, view):
        sms_name = request.query_params.get('type')
        sms_id = request.query_params.get('id')

        try:
            sms_ids = list(filter(None, sms_id.split(",")))
            # 对象集的权限验证(验证规则all)
            for obj in globals()['Dms{}Avg'.format(sms_name.title())].\
                    objects.filter(**{"__".join([f'{sms_name}_id', 'in']): sms_ids}):
                if not request.user.has_perm(f'view_dms{sms_name}avg', obj):
                    return False
            return True
        except Exception:  # 出现uncleaned数据交给filter来做处理
            return True

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class OnlinePermission(permissions.BasePermission):
    """
    实时工作数据 对象级权限
    """

    def has_permission(self, request, view):
        # 由于online表的数据量大，且经常变动，采用逻辑验证而不用对象级权限映射的方式
        user = request.user
        role_id = request.user.groups.all()[0].id
        sms_name = request.query_params.get('type')
        sms_id = request.query_params.get('id')
        if sms_name not in [sms_info[0] for sms_info in ONLINE_TYPE_CHOICES]:  # 出现uncleaned数据交给filter来做处理
            return True
        # 先判断总权限
        if not user.has_perm(f'dms.view_dms{sms_name}online'):
            return False
        try:
            # 再根据逻辑判断对象权限
            if role_id == 4:  # 总经理
                return True
            elif role_id == 3:  # 经理
                _id = Workshop.objects.get(employee=user.employee_id).id  # 获得经理管理车间号
                if sms_name in ["team", "group", "workshop"]:
                    for sms_obj in TeamGroupWorkshop.objects.filter(workshop=_id).values(sms_name).distinct():
                        if int(sms_id) == sms_obj[sms_name]:
                            return True
                    return False  # 没有该对象的权限
                elif sms_name == "stat":
                    for team_obj in TeamGroupWorkshop.objects.filter(workshop=_id).values('team').distinct():
                        team_id = team_obj['team']
                        # 取小组对应的最新十个工位信息
                        for stat_obj in get_recent_stat_obj(team_id):
                            stat_id = getattr(stat_obj, f"{sms_name}_id")
                            if int(sms_id) == stat_id:
                                return True
                    return False  # 没有该对象的权限
            elif role_id == 2:  # 大组长
                _id = Group.objects.get(employee=user.employee_id).id  # 获得大组长管理大组号
                if sms_name in ["team", "group"]:
                    for sms_obj in TeamGroupWorkshop.objects.filter(group=_id).values(sms_name).distinct():
                        if int(sms_id) == sms_obj[sms_name]:
                            return True
                    return False  # 没有该对象的权限
                elif sms_name == "stat":
                    for team_obj in TeamGroupWorkshop.objects.filter(group=_id).values('team').distinct():
                        team_id = team_obj['team']
                        # 取小组对应的最新十个工位信息
                        for stat_obj in get_recent_stat_obj(team_id):
                            stat_id = getattr(stat_obj, f"{sms_name}_id")
                            if int(sms_id) == stat_id:
                                return True
                    return False  # 没有该对象的权限
        except Exception:  # 出现uncleaned数据交给filter来做处理
            return True

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class DailyPermission(permissions.BasePermission):
    """
    历史工作数据 对象级权限
    """

    def has_permission(self, request, view):
        # 由于daily表的数据量大，且经常变动，采用逻辑验证而不用对象级权限映射的方式
        user = request.user
        role_id = request.user.groups.all()[0].id
        sms_name = request.query_params.get('type')
        sms_id = request.query_params.get('id')
        if sms_name not in [sms_info[0] for sms_info in DAILY_TYPE_CHOICES]:  # 出现uncleaned数据交给filter来做处理
            return True
        # 先判断总权限
        if not user.has_perm(f'dms.view_dms{sms_name}daily'):
            return False
        try:
            # 再根据逻辑判断对象权限
            if role_id == 4:  # 总经理
                return True
            elif role_id == 3:  # 经理
                _id = Workshop.objects.get(employee=user.employee_id).id  # 获得经理管理车间号
                if sms_name in ["team", "group", "workshop"]:
                    for sms_obj in TeamGroupWorkshop.objects.filter(workshop=_id).values(sms_name).distinct():
                        if int(sms_id) == sms_obj[sms_name]:
                            return True
                    return False  # 没有该对象的权限
                elif sms_name == "stat":
                    for team_obj in TeamGroupWorkshop.objects.filter(workshop=_id).values('team').distinct():
                        team_id = team_obj['team']
                        # 取小组对应的最新十个工位信息
                        for stat_obj in get_recent_stat_obj(team_id):
                            stat_id = getattr(stat_obj, f"{sms_name}_id")
                            if int(sms_id) == stat_id:
                                return True
                    return False  # 没有该对象的权限
                elif sms_name == "worker":
                    for team_obj in TeamGroupWorkshop.objects.filter(workshop=_id).values('team').distinct():
                        team_id = team_obj['team']
                        # 取小组对应的最新十个工位信息
                        for worker_obj in get_recent_stat_obj(team_id):
                            worker_ids = (getattr(worker_obj, "morning_shift_id"),
                                          getattr(worker_obj, "middle_shift_id"),
                                          getattr(worker_obj, "night_shift_id")
                                          )
                            if int(sms_id) in worker_ids:
                                return True
                    return False  # 没有该对象的权限
            elif role_id == 2:  # 大组长
                _id = Group.objects.get(employee=user.employee_id).id  # 获得大组长管理大组号
                if sms_name in ["team", "group"]:
                    for sms_obj in TeamGroupWorkshop.objects.filter(group=_id).values(sms_name).distinct():
                        if int(sms_id) == sms_obj[sms_name]:
                            return True
                    return False  # 没有该对象的权限
                elif sms_name == "stat":
                    for team_obj in TeamGroupWorkshop.objects.filter(group=_id).values('team').distinct():
                        team_id = team_obj['team']
                        # 取小组对应的最新十个工位信息
                        for stat_obj in get_recent_stat_obj(team_id):
                            stat_id = getattr(stat_obj, f"{sms_name}_id")
                            if int(sms_id) == stat_id:
                                return True
                    return False  # 没有该对象的权限
                elif sms_name == "worker":
                    for team_obj in TeamGroupWorkshop.objects.filter(group=_id).values('team').distinct():
                        team_id = team_obj['team']
                        # 取小组对应的最新十个工位信息
                        for worker_obj in get_recent_stat_obj(team_id):
                            worker_ids = (getattr(worker_obj, "morining_shift_id"),
                                          getattr(worker_obj, "middle_shift_id"),
                                          getattr(worker_obj, "night_shift_id")
                                          )
                            if int(sms_id) in worker_ids:
                                return True
                    return False  # 没有该对象的权限
        except Exception:  # 出现uncleaned数据交给filter来做处理
            return True

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class ReportExportPermission(permissions.BasePermission):

    # 根据用户的信息和提供的Post参数来验证是否有权限
    def has_permission(self, request, view):
        role_id = request.user.groups.all()[0].id  # role_id只可能为4, 3, 2
        if role_id == 4:  # 总经理
            return True

        try:
            _type = request.data["type"]
            if _type == "alert":  # 只有总经理可以导出警报排名
                return False
            all_id = request.data["all_id"].split(',')  # type: str
            if role_id == 3:  # 经理(不能导出dpt)
                return self.has_level_permission(request.user, _type, all_id, ["dpt"])
            elif role_id == 2:  # 大组长(不能导出dpt, workshop)
                return self.has_level_permission(request.user, _type, all_id, ["dpt", "workshop"])
        except Exception:
            return True
        return True

    @staticmethod
    def has_level_permission(user, _type, all_id, superiors):
        """
        :param user: 当前登录的用户（只可能是经理或大组长）
        :param _type: 任意
        :param all_id: 数字组成的字符串数组或all
        :param superiors: 所有上级
        :return: True, False
        """
        role = user.groups.all()[0].name  # 比如，经理
        employee_id = user.employee_id
        role_level = {
            "经理": "workshop",
            "大组长": "group"
        }
        if _type in superiors:  # 如果要导出上级的报表
            return False
        elif _type == role_level[role]:  # 如果要导出平级的报表
            # 获得所管理平级的id
            manage_struct_id = globals()[role_level[role].title()].objects.get(employee=employee_id).id
            if len(all_id) == 1 and int(all_id[0]) == manage_struct_id:
                return True
            else:
                return False
        else:  # 要导出下级的报表
            manage_struct_id = globals()[role_level[role].title()].objects.get(employee=employee_id).id
            all_managed_subordinates = None
            all_managed_subordinates_id = []  # 所有被当前用户管理的下级

            if _type == "worker":  # worker要用单独的逻辑处理
                all_managed_subordinates_id = get_all_worker_id(role_level[role], manage_struct_id)
            elif role == "经理":  # 当前用户是经理
                all_managed_subordinates = TeamGroupWorkshop.objects \
                    .filter(workshop_id=manage_struct_id).values(_type).distinct()
            elif role == "大组长":  # 当前用户是大组长
                all_managed_subordinates = TeamGroupWorkshop.objects \
                    .filter(group_id=manage_struct_id).values(_type).distinct()

            if len(all_managed_subordinates_id) == 0:
                for item in all_managed_subordinates:
                    all_managed_subordinates_id.append(item[_type])

            for _id in all_id:
                if int(_id) not in all_managed_subordinates_id:
                    return False
            return True


class AlertTransferPermission(permissions.BasePermission):
    """
    警报传递信息 对象级权限
    """
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        role_id = request.user.groups.all()[0].id
        if role_id == 4:  # 总经理/管理员
            return True

        if obj.alert_convey_info.filter(deal_employee_id=request.user.employee_id):
            return True
        return False


class AlertConfPermission(permissions.BasePermission):
    """
    cfg中的警报条件数据和警报传递数据 对象级权限
    """
    def has_permission(self, request, view):
        role_id = request.user.groups.all()[0].id
        if role_id == 4:  # 总经理/管理员
            return True
        for perm_codename in view.permission_codename:  # 对象级权限验证
            if not request.user.has_perm(perm_codename):
                return False
        return True
