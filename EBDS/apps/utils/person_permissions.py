# coding: utf-8
from rest_framework import permissions
from standard.models import StandardTeam, StandardGroup, StandardWorkshop, StandardDpt


class StandardPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        sms_name = request.query_params.get('type')
        sms_id = request.query_params.get('id')

        try:
            obj = globals()['Standard' + sms_name.title()].objects.get(**{sms_name: sms_id})
            return request.user.has_perm(f'view_standard{sms_name}', obj)
        except Exception:  # 出现uncleaned数据交给filter来做处理
            return True

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.user == request.user
