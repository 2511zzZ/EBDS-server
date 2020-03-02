from rest_framework import status
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

from utils.person_permissions import AlertConfPermission
from .models import CfgUserInquiry, CfgAlertCondition, CfgAlertTransfer
from .serializers import UserInquirySerializer, CfgAlertConditionSerializer, \
    CfgAlertTransferSerializer


class UserConfViewset(mixins.ListModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """
    用户设置(list/update)
    """
    queryset = CfgUserInquiry.objects.all()
    serializer_class = UserInquirySerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user_id = self.request.user.id
        user_cfg_query_set = self.get_queryset().filter(user_id=user_id)
        if len(user_cfg_query_set) != 0:
            user_cfg_obj = user_cfg_query_set[0]
        else:
            user_cfg_obj = None
        return user_cfg_obj

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response("数据库中没有该用户的设置", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AlertConditionViewset(mixins.ListModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """
    警报条件数据
    """
    queryset = CfgAlertCondition.objects.all()
    serializer_class = CfgAlertConditionSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, AlertConfPermission)
    permission_codename = ["cfg.view_cfgalertcondition", "cfg.change_cfgalertcondition"]

    def get_object(self):
        return CfgAlertCondition.objects.all()[0]  # 只有一条配置


class AlertTransferViewset(mixins.ListModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """
    警报传递数据
    """
    queryset = CfgAlertTransfer.objects.all()
    serializer_class = CfgAlertTransferSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, AlertConfPermission)
    permission_codename = ["cfg.view_cfgalerttransfer", "cfg.change_cfgalerttransfer"]

    def get_object(self):
        return CfgAlertTransfer.objects.all()[0]  # 只有一条配置
