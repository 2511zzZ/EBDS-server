# coding: utf-8
"""
自定义的django-filter字段
"""
import django_filters


class ListFilter(django_filters.CharFilter):
    """
    根据分隔符可传递多个值的字段
    """
    def filter(self, qs, value):
        value = list(filter(None, value.split(",")))
        return super().filter(qs=qs, value=value)


