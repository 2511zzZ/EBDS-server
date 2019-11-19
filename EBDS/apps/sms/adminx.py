# coding: utf-8
import xadmin
from .models import Member, Team, Group, Workshop, TeamGroupWorkshop, TeamStatMember


class MemberAdmin(object):
    list_display = ['employee_id', 'name', 'sex', 'birthday', 'birthplace', 'type']
    search_fields = ['employee_id', 'name', 'birthplace']
    list_editable = ["type", ]
    list_filter = ['name', 'sex', 'birthday', 'birthplace', 'type']
    ordering = ['employee_id']
    # style_fields = {"goods_desc": "ueditor"}


class TeamAdmin(object):
    list_display = ["id", "name"]
    ordering = ['id']


class GroupAdmin(object):
    list_display = ["id", "name", "employee"]
    ordering = ['id']


class WorkshopAdmin(object):
    list_display = ["id", "name", "employee"]
    ordering = ['id']


class TeamGroupWorkshopAdmin(object):
    list_display = ["team", "group", "workshop"]
    ordering = ['id']


class TeamStatMemberAdmin(object):
    list_display = ["team", "stat_id", "morning_shift_id", "middle_shift_id", "night_shift_id", "update_time"]
    ordering = ['update_time', 'team']



xadmin.site.register(Member, MemberAdmin)
xadmin.site.register(Team, TeamAdmin)
xadmin.site.register(Group, GroupAdmin)
xadmin.site.register(Workshop, WorkshopAdmin)

xadmin.site.register(TeamGroupWorkshop, TeamGroupWorkshopAdmin)
xadmin.site.register(TeamStatMember, TeamStatMemberAdmin)

