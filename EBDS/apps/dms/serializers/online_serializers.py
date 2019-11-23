# coding: utf-8

from ..models import DmsTeamOnline, DmsGroupOnline, DmsWorkshopOnline, DmsDptOnline, DmsStatOnline
from utils.person_serializers import OnlineSerializer, DmsListSerializer


class DmsTeamOnlineSerializer(OnlineSerializer):

    class Meta:
        model = DmsTeamOnline
        list_serializer_class = DmsListSerializer
        fields = ('team_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsGroupOnlineSerializer(OnlineSerializer):

    class Meta:
        model = DmsGroupOnline
        list_serializer_class = DmsListSerializer
        fields = ('group_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsWorkshopOnlineSerializer(OnlineSerializer):

    class Meta:
        model = DmsWorkshopOnline
        list_serializer_class = DmsListSerializer
        fields = ('workshop_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsDptOnlineSerializer(OnlineSerializer):

    class Meta:
        model = DmsDptOnline
        list_serializer_class = DmsListSerializer
        fields = ('dpt_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsStatOnlineSerializer(OnlineSerializer):

    class Meta:
        model = DmsStatOnline
        list_serializer_class = DmsListSerializer
        fields = ('stat_id', 'efficiency', 'accuracy', 'workhour', 'time')

