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
from .filters.avg_filters import AverageFilter
from utils.person_permissions import AveragePermission


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








