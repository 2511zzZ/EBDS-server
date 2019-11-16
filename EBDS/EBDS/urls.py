# coding=utf-8
"""EBDS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
import xadmin
from .settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path, re_path, include

route = DefaultRouter()

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    re_path(r"^", include(route.urls)),
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),

    path("docs/", include_docs_urls("流水线行为检测系统API接口文档")),
    re_path(r"^api_auth", include("rest_framework.urls")),
    # jwt的认证接口
    re_path(r'^login/', obtain_jwt_token),
]
