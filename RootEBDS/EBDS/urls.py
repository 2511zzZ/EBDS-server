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

from core.Router import NoLookupUpdateRouter
from standard.router import standard_router
from dms.router import dms_router
from sms.router import sms_router
from users.router import user_router

route = DefaultRouter()
route.registry.extend(standard_router.registry)
route.registry.extend(dms_router.registry)
route.registry.extend(sms_router.registry)
# route.registry.extend(user_router.registry)

# 改变mine/的update和partial_update默认路由地址(
# mine/和avatar/不会显示在api root中,
# 因为只会对第一个DefaultRouter返回的url生效)
user_route = NoLookupUpdateRouter()
user_route.registry.extend(user_router.registry)


urlpatterns = [
    re_path(r"^", include(route.urls)),
    re_path(r"^", include(user_route.urls)),
    path('xadmin/', xadmin.site.urls),
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    path("docs/", include_docs_urls("流水线行为检测系统API接口文档")),
    re_path(r"^api_auth", include("rest_framework.urls")),
    # jwt的认证接口
    re_path(r'^login/', obtain_jwt_token),
]

