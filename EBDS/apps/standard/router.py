# coding: utf-8

from .views import StandardViewset
from rest_framework.routers import DefaultRouter

standard_router = DefaultRouter()

standard_router.register(r'standard', StandardViewset, base_name="standard")

