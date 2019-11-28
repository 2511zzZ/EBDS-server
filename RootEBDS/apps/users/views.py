from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserDetailSerializer

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



