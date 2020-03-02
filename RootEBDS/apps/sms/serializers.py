# coding: utf-8
from django.db.models import Q
from .models import Member, Team, Group, Workshop, TeamStatMember, TeamGroupWorkshop
from rest_framework import serializers
from utils.static_methods import get_recent_employee_stat_obj


class TeamSerializer(serializers.ModelSerializer):
    # https://www.django-rest-framework.org/community/3.0-announcement/#optional-argument-to-serializermethodfield
    team_name = serializers.SerializerMethodField()

    class Meta:
        model = TeamGroupWorkshop
        fields = ('team', 'team_name', 'group', 'workshop')

    def get_team_name(self, obj):
        return obj.team.name


class GroupSerializer(serializers.ModelSerializer):
    # https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#updating-our-serializer
    group_name = serializers.ReadOnlyField(source='group.name')
    group_manager = serializers.ReadOnlyField(source='group.employee.employee_id')
    group_manager_name = serializers.ReadOnlyField(source='group.employee.name')

    class Meta:
        model = TeamGroupWorkshop
        fields = ('group', 'group_name', 'group_manager', 'group_manager_name', 'workshop')


class WorkshopSerializer(serializers.ModelSerializer):
    workshop_name = serializers.ReadOnlyField(source='workshop.name')
    workshop_manager = serializers.ReadOnlyField(source='workshop.employee.employee_id')
    workshop_manager_name = serializers.ReadOnlyField(source='workshop.employee.name')

    class Meta:
        model = TeamGroupWorkshop
        fields = ('workshop', 'workshop_name', 'workshop_manager', 'workshop_manager_name')


class StatSerializer(serializers.ModelSerializer):
    stat = serializers.ReadOnlyField(source='stat_id')
    team_name = serializers.ReadOnlyField(source='team.name')
    morning_shift_name = serializers.SerializerMethodField()
    middle_shift_name = serializers.SerializerMethodField()
    night_shift_name = serializers.SerializerMethodField()

    class Meta:
        model = TeamStatMember
        fields = ('stat', 'morning_shift_id', 'morning_shift_name',
                  'middle_shift_id', 'middle_shift_name',
                  'night_shift_id', 'night_shift_name',
                  'team', 'team_name')

    def get_morning_shift_name(self, obj):
        return Member.objects.get(employee_id=obj.morning_shift_id).name

    def get_middle_shift_name(self, obj):
        return Member.objects.get(employee_id=obj.middle_shift_id).name

    def get_night_shift_name(self, obj):
        return Member.objects.get(employee_id=obj.night_shift_id).name


class WorkerSerializer(serializers.ModelSerializer):
    employee = serializers.ReadOnlyField(source='employee_id')
    stat = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = ('employee', 'name', 'sex', 'birthplace', 'stat', 'team')

    def get_stat(self, obj):
        """所属工位号"""
        employee_id = obj.employee_id
        # 返回员工目前所在的工位
        stat_obj = get_recent_employee_stat_obj(employee_id)
        return stat_obj.stat_id

    def get_team(self, obj):
        """所属小组号"""
        employee_id = obj.employee_id
        # 返回员工目前所在的工位
        stat_obj = get_recent_employee_stat_obj(employee_id)
        return stat_obj.team_id

