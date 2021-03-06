# coding: utf-8

import django_filters
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from .models import StandardTeam, StandardGroup, StandardWorkshop, StandardDpt
from core.choices import STANDARD_TYPE_CHOICES, METRIC_CHOICES
from utils.person_filter import ListFilter
from utils.static_methods import get_recent_stat_team_id, get_recent_worker_team_id


class StandardFilter(django_filters.rest_framework.FilterSet):
    """
    所有标准的通用过滤类
    """
    type = django_filters.ChoiceFilter(method='type_filter', help_text='标准类型', choices=STANDARD_TYPE_CHOICES, required=True,
                                       error_messages={
                                          "required": "参数缺失!",
                                       }
                                       )
    id = ListFilter(method='id_filter', help_text='id',
                    required=True, error_messages={
                         "required": "参数缺失!",
                    }
                    )
    metric = django_filters.ChoiceFilter(method='metric_filter', choices=METRIC_CHOICES, help_text='数据类型')

    def type_filter(self, queryset, name, value):
        # self.Meta.model = globals()["Standard"+value.title()]  # 动态指定model
        return queryset

    def id_filter(self, queryset, name, value):
        if self.request.query_params["type"] == "dpt":
            return queryset

        try:
            value = list(filter(None, value.split(",")))  # 当filter第一个参数为None,会把"False"值全部丢弃
            if self.request.query_params["type"] == 'stat':
                return queryset.filter(pk__in=get_recent_stat_team_id(value))
            elif self.request.query_params["type"] == 'worker':
                return queryset.filter(pk__in=get_recent_worker_team_id(value))
            return queryset.filter(pk__in=value)
        except Exception as e:
            error_msg = {"invalid": "请检查字段信息!"}
            msg = {"id": error_msg["invalid"]}
            raise ValidationError(msg, code='invalid')

    def metric_filter(self, queryset, name, value):
        # 交给Serializer来过滤字段
        return queryset   # such as s_efficiency

    class Meta:
        # model = Goods
        fields = ['type', 'id', 'metric']
