from django.core import serializers

from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import DmsTeamAvg, DmsGroupAvg, DmsWorkshopAvg, DmsDptAvg, DmsStatAvg
from .serializers import DmsTeamAvgSerializer, DmsGroupAvgSerializer, DmsWorkshopAvgSerializer, \
    DmsDptAvgSerializer, DmsStatAvgSerializer

from .models import DmsTeamOnline, DmsGroupOnline, DmsWorkshopOnline, DmsDptOnline, DmsStatOnline
from .serializers import DmsTeamOnlineSerializer, DmsGroupOnlineSerializer, DmsWorkshopOnlineSerializer, \
    DmsDptOnlineSerializer, DmsStatOnlineSerializer

from .filters.avg_filters import AverageFilter
from .filters.online_filters import OnlineFilter
from utils.person_permissions import AveragePermission, OnlinePermission


class AverageViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    实时平均工作数据
    """
    serializer_class = DmsTeamAvgSerializer
    queryset = DmsTeamAvg.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    filter_backends = (DjangoFilterBackend, )
    permission_classes = (IsAuthenticated, AveragePermission)
    filter_class = AverageFilter

    def get_serializer_class(self):
        try:
            return globals()[f"Dms{self.request.query_params.get('type').title()}AvgSerializer"]
        except (KeyError, AttributeError):  # 出现uncleaned数据交给filter来做处理
            return self.serializer_class

    def get_queryset(self):
        try:
            model_name = globals()[f"Dms{self.request.query_params.get('type').title()}Avg"]
            return model_name.objects.all()
        except (KeyError, AttributeError):  # 出现uncleaned数据交给filter来做处理
            return self.queryset


class OnlineViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    实时工作数据
    """
    serializer_class = DmsTeamOnline
    queryset = DmsTeamOnline.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated, OnlinePermission)
    filter_class = OnlineFilter

    def get_serializer_class(self):
        try:
            return globals()[f"Dms{self.request.query_params.get('type').title()}OnlineSerializer"]
        except (KeyError, AttributeError):  # 出现uncleaned数据交给filter来做处理
            return self.serializer_class

    def get_queryset(self):
        try:
            model_name = globals()[f"Dms{self.request.query_params.get('type').title()}Online"]
            return model_name.objects.all()
        except (KeyError, AttributeError):  # 出现uncleaned数据交给filter来做处理
            return self.queryset







