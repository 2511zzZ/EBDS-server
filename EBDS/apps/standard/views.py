from django.core import serializers

from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import StandardTeam, StandardGroup, StandardWorkshop, StandardDpt
from .serializers import StandardTeamSerializer, StandardGroupSerializer, \
    StandardWorkshopSerializer, StandardDptSerializer
from .filters import StandardFilter
from utils.person_permissions import StandardPermission


class StandardViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    标准指标
    """
    serializer_class = StandardTeamSerializer
    queryset = StandardTeam.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    filter_backends = (DjangoFilterBackend, )
    permission_classes = (IsAuthenticated, StandardPermission)
    filter_class = StandardFilter

    def get_serializer_class(self):
        try:
            return globals()["Standard" + self.request.query_params.get('type').title() + "Serializer"]
        except (KeyError, AttributeError):  # 出现uncleaned数据交给filter来做处理
            return self.serializer_class

    def get_queryset(self):
        try:
            model_name = globals()["Standard" + self.request.query_params.get('type').title()]
            return model_name.objects.all()
        except (KeyError, AttributeError):  # 出现uncleaned数据交给filter来做处理
            return self.queryset








