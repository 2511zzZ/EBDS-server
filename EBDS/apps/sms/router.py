# coding: utf-8

from .views import TeamViewset, GroupViewset, WorkshopViewset, StatViewset, WorkerViewset
from rest_framework.routers import DefaultRouter

sms_router = DefaultRouter()

sms_router.register(r'team', TeamViewset, base_name="team")
sms_router.register(r'group', GroupViewset, base_name="group")
sms_router.register(r'workshop', WorkshopViewset, base_name="workshop")
sms_router.register(r'stat', StatViewset, base_name="stat")
sms_router.register(r'worker', WorkerViewset, base_name="worker")
