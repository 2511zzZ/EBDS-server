from django.core import serializers
from django.db.models.expressions import RawSQL
from django.db.models import Max

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

from .models import TeamGroupWorkshop, TeamStatMember, Group, Workshop
from .serializers import TeamSerializer, GroupSerializer, WorkshopSerializer, StatSerializer
from .filters import TeamFilter, GroupFilter, WorkshopFilter, StatFilter
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


class StatViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    工位查询
    """
    queryset = TeamStatMember.objects.all()
    serializer_class = StatSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    permission_classes = (IsAuthenticated,)
    filter_class = StatFilter
    ordering_fields = ('stat_id', 'team')
    ordering = ('stat_id',)

    def get_queryset(self):
        user = self.request.user
        role_id = user.groups.all()[0].id
        if role_id == 4:
            # 每个工位记录分组中时间最近的那一条记录
            # 子查询逻辑复杂，用django_orm表示难度太大
            # func1:因为raw()返回的数据集是RawQuerySet不能直接使用，所以这里用filter结合RawSQL
            # func2:必须把这条语句写成ORM！因为用了RawSQL就不会惰性查询！耗费了大量的查询时间在get_queryset上
            # func3:返回分组后的最大id,只要变更时间一直是递增的就不会出问题,并且也符合业务场景
            # func3 mysql sql:
            # SELECT * FROM sms_team_stat_member
            # WHERE id in (SELECT MAX(id) FROM sms_team_stat_member GROUP BY stat_id);
            return self.queryset.filter(id__in=
                                        self.queryset.values('stat_id').
                                        annotate(default_id=Max('id')).
                                        values('default_id')
                                        )
        elif role_id == 3:  # 经理
            _id = Workshop.objects.get(employee=user.employee_id).id  # 获得经理管理车间号
            team_id_objs = TeamGroupWorkshop.objects.filter(workshop=_id).values('team')
            return self.queryset.filter(id__in=
                                        self.queryset.values('stat_id').
                                        annotate(default_id=Max('id')).
                                        values('default_id')
                                        ).filter(team__in=team_id_objs)

        elif role_id == 2:  # 大组长
            _id = Group.objects.get(employee=user.employee_id).id  # 获得大组长管理大组号
            team_id_objs = TeamGroupWorkshop.objects.filter(group=_id).values('team')
            return self.queryset.filter(id__in=
                                        self.queryset.values('stat_id').
                                        annotate(default_id=Max('id')).
                                        values('default_id')
                                        ).filter(team__in=team_id_objs)







