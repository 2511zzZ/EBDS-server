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
