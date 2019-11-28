# coding: utf-8

from ..models import DmsTeamAvg, DmsGroupAvg, DmsWorkshopAvg, DmsDptAvg, DmsStatAvg
from utils.person_serializers import AverageSerializer


class DmsTeamAvgSerializer(AverageSerializer):

    class Meta:
        model = DmsTeamAvg
        fields = ('team_id', 'a_efficiency', 'a_accuracy', 'a_workhour', 'time')


class DmsGroupAvgSerializer(AverageSerializer):

    class Meta:
        model = DmsGroupAvg
        fields = ('group_id', 'a_efficiency', 'a_accuracy', 'a_workhour', 'time')


class DmsWorkshopAvgSerializer(AverageSerializer):

    class Meta:
        model = DmsWorkshopAvg
        fields = ('workshop_id', 'a_efficiency', 'a_accuracy', 'a_workhour', 'time')


class DmsDptAvgSerializer(AverageSerializer):

    class Meta:
        model = DmsDptAvg
        fields = ('dpt_id', 'a_efficiency', 'a_accuracy', 'a_workhour', 'time')


class DmsStatAvgSerializer(AverageSerializer):

    class Meta:
        model = DmsStatAvg
        fields = ('stat_id', 'a_efficiency', 'a_accuracy', 'a_workhour', 'time')

