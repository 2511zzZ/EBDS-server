# coding: utf-8
from django.db.models import Max
from rest_framework import permissions
from standard.models import StandardTeam, StandardGroup, StandardWorkshop, StandardDpt

from dms.models import DmsTeamAvg, DmsGroupAvg, DmsWorkshopAvg, DmsDptAvg, DmsStatAvg

from dms.models import DmsTeamOnline, DmsGroupOnline, DmsWorkshopOnline, DmsDptOnline, DmsStatOnline

from sms.models import Team, Group, Workshop, Dpt, TeamStatMember, TeamGroupWorkshop

from core.choices import ONLINE_TYPE_CHOICES, DAILY_TYPE_CHOICES


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
    @staticmethod
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
                        for stat_obj in self.get_recent_stat_obj(team_id):
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
                        for stat_obj in self.get_recent_stat_obj(team_id):
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
    @staticmethod
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
                        for stat_obj in self.get_recent_stat_obj(team_id):
                            stat_id = getattr(stat_obj, f"{sms_name}_id")
                            if int(sms_id) == stat_id:
                                return True
                    return False  # 没有该对象的权限
                elif sms_name == "worker":
                    for team_obj in TeamGroupWorkshop.objects.filter(workshop=_id).values('team').distinct():
                        team_id = team_obj['team']
                        # 取小组对应的最新十个工位信息
                        for worker_obj in self.get_recent_stat_obj(team_id):
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
                        for stat_obj in self.get_recent_stat_obj(team_id):
                            stat_id = getattr(stat_obj, f"{sms_name}_id")
                            if int(sms_id) == stat_id:
                                return True
                    return False  # 没有该对象的权限
                elif sms_name == "worker":
                    for team_obj in TeamGroupWorkshop.objects.filter(group=_id).values('team').distinct():
                        team_id = team_obj['team']
                        # 取小组对应的最新十个工位信息
                        for worker_obj in self.get_recent_stat_obj(team_id):
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
