# coding: utf-8

from .views import ReportFileViewset
from rest_framework.routers import DefaultRouter

report_export_router = DefaultRouter()

report_export_router.register(r'report_file', ReportFileViewset, base_name="report_file")

