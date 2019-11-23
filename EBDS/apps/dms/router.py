# coding: utf-8

from .views import AverageViewset, OnlineViewset
from rest_framework.routers import DefaultRouter

dms_router = DefaultRouter()

dms_router.register(r'averages', AverageViewset, base_name="averages")
dms_router.register(r'online_data', OnlineViewset, base_name='online_data')
