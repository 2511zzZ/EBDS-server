# coding: utf-8

from .views import UserDetailViewset, AvatarViewset
from rest_framework.routers import DefaultRouter

user_router = DefaultRouter()

user_router.register(r'mine', UserDetailViewset, base_name="mine")
user_router.register(r'avatar', AvatarViewset, base_name="avatar")

