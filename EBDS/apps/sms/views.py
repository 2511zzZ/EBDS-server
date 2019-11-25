from django.core import serializers

from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import TeamGroupWorkshop
from .serializers import TeamSerializer, GroupSerializer, WorkshopSerializer
from .filters import TeamFilter, GroupFilter, WorkshopFilter
from core.pagination import StandardResultsSetPagination
from utils.person_filter import TeamGroupWorkshopFilterBackend


class TeamViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    小组查询
    """
    queryset = TeamGroupWorkshop.objects.all()
    serializer_class = TeamSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # HACK:这里也可以覆盖get_queryset来做，但不能复用；也能用permission来做，但与业务逻辑不太相符
    filter_backends = (TeamGroupWorkshopFilterBackend,
                       DjangoFilterBackend, filters.OrderingFilter)
    permission_classes = (IsAuthenticated,)
    filter_class = TeamFilter
    ordering_fields = ('team', 'group', 'workshop')
    ordering = ('team',)  # stackoverflow.com/questions/44033670/python-django-rest-framework-unorderedobjectlistwarning


class GroupViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    大组查询
    """
    queryset = TeamGroupWorkshop.objects.all()
    serializer_class = GroupSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # HACK:这里也可以覆盖get_queryset来做，但不能复用；也能用permission来做，但与业务逻辑不太相符
    filter_backends = (TeamGroupWorkshopFilterBackend,
                       DjangoFilterBackend, filters.OrderingFilter)
    permission_classes = (IsAuthenticated,)
    filter_class = GroupFilter
    ordering_fields = ('group', 'workshop')
    ordering = ('group',)


class WorkshopViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    车间查询
    """
    queryset = TeamGroupWorkshop.objects.all()
    serializer_class = WorkshopSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # HACK:这里也可以覆盖get_queryset来做，但不能复用；也能用permission来做，但与业务逻辑不太相符
    filter_backends = (TeamGroupWorkshopFilterBackend,
                       DjangoFilterBackend, filters.OrderingFilter)
    permission_classes = (IsAuthenticated,)
    filter_class = WorkshopFilter
    ordering = ordering_fields = ('workshop',)







