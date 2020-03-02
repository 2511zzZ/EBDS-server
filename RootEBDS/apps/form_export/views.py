# coding: utf-8
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.person_permissions import ReportExportPermission

from rest_framework.request import Request
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status

from .serializers import FormSerializer


class ReportFileViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = FormSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # TODO认证改回去
    permission_classes = (IsAuthenticated, ReportExportPermission)

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})  # 实例化一个serializer对象
        serializer.is_valid(raise_exception=True)  # 对序列化类中的字段进行验证

        # perform_create调用序列化实例的save()方法，在save()中会调用
        # 序列化类中的create或update(这里没有用到)方法。一般情况下会往数据库插入数据。
        # 像这样：return ExampleModel.objects.create(**validated_data)
        # 而在这里则返回一个叫instance的变量，变量中返回一个创建好了的文件url。
        path_json = self.perform_create(serializer)
        # print(serializer.data)

        if 'error' in path_json:
            return Response(path_json, status=status.HTTP_400_BAD_REQUEST)
        return Response(path_json, status=status.HTTP_201_CREATED)
