# coding: utf-8

from .views import AverageViewset
from rest_framework.routers import DefaultRouter

average_router = DefaultRouter()

average_router.register(r'averages', AverageViewset, base_name="averages")
