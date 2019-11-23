# coding: utf-8

from ..models import DmsTeamDaily, DmsGroupDaily, DmsWorkshopDaily, DmsDptDaily, \
    DmsStatDaily, DmsWorkerDaily
from utils.person_serializers import DailySerializer, DmsListSerializer


class DmsTeamDailySerializer(DailySerializer):

    class Meta:
        model = DmsTeamDaily
        list_serializer_class = DmsListSerializer
        fields = ('team_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsGroupDailySerializer(DailySerializer):

    class Meta:
        model = DmsGroupDaily
        list_serializer_class = DmsListSerializer
        fields = ('group_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsWorkshopDailySerializer(DailySerializer):

    class Meta:
        model = DmsWorkshopDaily
        list_serializer_class = DmsListSerializer
        fields = ('workshop_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsDptDailySerializer(DailySerializer):

    class Meta:
        model = DmsDptDaily
        list_serializer_class = DmsListSerializer
        fields = ('dpt_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsStatDailySerializer(DailySerializer):

    class Meta:
        model = DmsStatDaily
        list_serializer_class = DmsListSerializer
        fields = ('stat_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsWorkerDailySerializer(DailySerializer):

    class Meta:
        model = DmsWorkerDaily
        list_serializer_class = DmsListSerializer
        fields = ('worker_id', 'efficiency', 'accuracy', 'workhour', 'time')
