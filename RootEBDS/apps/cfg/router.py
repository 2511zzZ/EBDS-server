# coding: utf-8

from .views import UserConfViewset, AlertConditionViewset, AlertTransferViewset
from rest_framework.routers import DefaultRouter

user_conf_router = DefaultRouter()

user_conf_router.register(r'user_conf', UserConfViewset, base_name="user_conf")
user_conf_router.register(r'alert_condition_conf', AlertConditionViewset, base_name="alert_condition_conf")
user_conf_router.register(r'alert_transfer_conf', AlertTransferViewset, base_name="alert_transfer_conf")

