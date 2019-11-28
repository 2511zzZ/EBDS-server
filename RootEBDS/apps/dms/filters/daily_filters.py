# coding: utf-8
import django_filters
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError

from ..models import DmsTeamDaily, DmsGroupDaily, DmsWorkshopDaily, DmsDptDaily, \
    DmsStatDaily, DmsWorkerDaily
from core.choices import DAILY_TYPE_CHOICES, METRIC_CHOICES
from utils.person_filter import ListFilter


class DailyFilter(django_filters.rest_framework.FilterSet):
    """
    所有历史工作数据的通用过滤类
    """
    type = django_filters.ChoiceFilter(method='type_filter', help_text='标准类型',
                                       choices=DAILY_TYPE_CHOICES, required=True,
                                       error_messages={
                                           "required": "参数缺失!",
                                       }
                                       )
    id = django_filters.NumberFilter(method='id_filter', help_text='id',
                                     required=True, error_messages={
                                         "required": "参数缺失!",
                                     }
                                     )
    metric = django_filters.ChoiceFilter(method='metric_filter', choices=METRIC_CHOICES, help_text='数据类型',
                                         required=True, error_messages={
                                             "required": "参数缺失!",
                                         }
                                         )
    start = django_filters.DateFilter(field_name='time', lookup_expr='gte', required=True, help_text='开始时间',
                                      error_messages={
                                             "required": "参数缺失!",
                                         })

    end = django_filters.DateFilter(field_name='time', lookup_expr='lte', required=True, help_text='结束时间',
                                    error_messages={
                                             "required": "参数缺失!",
                                         })

    def type_filter(self, queryset, name, value):
        self.Meta.model = globals()[f"Dms{value.title()}Daily"]  # 动态指定model
        return queryset

    def id_filter(self, queryset, name, value):
        sms_type = self.request.query_params["type"]
        if sms_type == "dpt":
            return queryset
        return queryset.filter(**{f'{sms_type}_id': value})

    def metric_filter(self, queryset, name, value):
        # 交给Serializer来过滤字段
        return queryset  # such as s_efficiency

    class Meta:
        fields = ['type', 'id', 'metric', 'start', 'end']



