# coding: utf-8
from .views import AlertDetailViewset, AlertOverviewView, AlertTransferView
from rest_framework.routers import DefaultRouter

ams_router = DefaultRouter()

ams_router.register(r'alert', AlertDetailViewset, base_name="alert")
ams_router.register(r'alert_overview', AlertOverviewView, base_name="alert_overview")
ams_router.register(r'alert_transfer', AlertTransferView, base_name="alert_transfer")
