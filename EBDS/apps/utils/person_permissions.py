# coding: utf-8
from rest_framework import permissions
from standard.models import StandardTeam, StandardGroup, StandardWorkshop, StandardDpt

from dms.models import DmsTeamAvg, DmsGroupAvg, DmsWorkshopAvg, DmsDptAvg, DmsStatAvg


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
