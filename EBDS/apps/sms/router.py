# coding: utf-8

from .views import TeamViewset, GroupViewset, WorkshopViewset
from rest_framework.routers import DefaultRouter

sms_router = DefaultRouter()

sms_router.register(r'team', TeamViewset, base_name="team")
sms_router.register(r'group', GroupViewset, base_name="group")
sms_router.register(r'workshop', WorkshopViewset, base_name="workshop")