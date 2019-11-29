from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserDetailSerializer, AvatarSerializer

User = get_user_model()


class UserDetailViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    登录用户信息
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AvatarViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    头像上传
    """
    serializer_class = AvatarSerializer
    # 以multipart/form-data方式post，把文件解析器的处理交给ImageField
    # parser_classes = (FileUploadParser,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        img_json = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if 'error' in img_json:
            return Response(img_json, status=status.HTTP_400_BAD_REQUEST)
        return Response(img_json, status=status.HTTP_201_CREATED, headers=headers)



