# coding: utf-8

from .views import UserDetailViewset
from rest_framework.routers import DefaultRouter

user_router = DefaultRouter()

user_router.register(r'mine', UserDetailViewset, base_name="mine")

