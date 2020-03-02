# coding: utf-8

from rest_framework import serializers
from .models import StandardTeam, StandardGroup, StandardWorkshop, StandardDpt
from utils.person_serializers import StandardSerializer


class StandardStatSerializer(StandardSerializer):
    # 要更改返回结果的team_id为stat_id可以改写get_fields方法
    # stat = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StandardTeam
        # fields = ('stat', 's_efficiency', 's_accuracy', 's_workhour')
        fields = '__all__'


class StandardWorkerSerializer(StandardSerializer):
    class Meta:
        model = StandardTeam
        fields = '__all__'


class StandardTeamSerializer(StandardSerializer):

    class Meta:
        model = StandardTeam
        fields = "__all__"


class StandardGroupSerializer(StandardSerializer):

    class Meta:
        model = StandardGroup
        fields = "__all__"


class StandardWorkshopSerializer(StandardSerializer):

    class Meta:
        model = StandardWorkshop
        fields = "__all__"


class StandardDptSerializer(StandardSerializer):

    class Meta:
        model = StandardDpt
        fields = "__all__"

