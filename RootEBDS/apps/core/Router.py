# coding: utf-8
from rest_framework.routers import Route, DynamicRoute, SimpleRouter, DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import APIRootView, SchemaView, SchemaGenerator, api_settings, OrderedDict
from django.urls import include, re_path


def url(regex, view, kwargs=None, name=None):
    return re_path(regex, view, kwargs, name)


class NoLookupUpdateRouter(SimpleRouter):
    """
    A router no {loopup} for mine Update
    https://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    """
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create',
                'put': 'update',
                'patch': 'partial_update',
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',

                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]


