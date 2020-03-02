from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.pagination import StandardResultsSetPagination
from .serializers import AmsBaseInfoSerializer, AmsDetailInfoSerializer, AmsOverviewSerializer, \
    AmsTransferSerializer
from .models import AmsConveyInfo, AmsBaseInfo
from .filters import AlertDetailFilter
from utils.person_permissions import AlertTransferPermission

User = get_user_model()


class AlertDetailViewset(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    警报详细信息
    """
    queryset = AmsConveyInfo.objects.all()
    serializer_class = AmsDetailInfoSerializer
    pagination_class = StandardResultsSetPagination     # 请求status为1时设置page_size以显示更多警报
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = AlertDetailFilter

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return AmsBaseInfoSerializer
        else:
            return AmsDetailInfoSerializer

    def get_queryset(self):
        user = self.request.user

        if self.action in ('update', 'partial_update'):
            AlertDetailViewset.filter_class = None  # 更新操作不需要过滤器
            return AmsBaseInfo.objects.all()
        else:
            AlertDetailViewset.filter_class = AlertDetailFilter
        return self.queryset.filter(deal_employee_id=user.employee_id)


class AlertTransferView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    警报传递信息
    """
    queryset = AmsBaseInfo.objects.all()
    serializer_class = AmsTransferSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 自定义了警报传递信息的权限验证
    permission_classes = (IsAuthenticated, AlertTransferPermission)


class AlertOverviewView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    警报总览信息(包括待办数/当月完成任务数/当月任务平均处理时间等)
    """
    serializer_class = AmsOverviewSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # 每个用户都有警报总览信息
        return User.objects.filter(username=self.request.user.username)

