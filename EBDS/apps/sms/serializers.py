# coding: utf-8

from .models import Member, Team, Group, Workshop, TeamStatMember, TeamGroupWorkshop
from rest_framework import serializers


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
    group_manager = serializers.ReadOnlyField(source='group.employee.id')
    group_manager_name = serializers.ReadOnlyField(source='group.employee.name')

    class Meta:
        model = TeamGroupWorkshop
        fields = ('group', 'group_name', 'group_manager', 'group_manager_name', 'workshop')


class WorkshopSerializer(serializers.ModelSerializer):
    workshop_name = serializers.ReadOnlyField(source='workshop.name')
    workshop_manager = serializers.ReadOnlyField(source='workshop.employee.id')
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
