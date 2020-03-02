# coding: utf-8
import django_filters
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError

from ..models import DmsTeamOnline, DmsGroupOnline, DmsWorkshopOnline, DmsDptOnline, DmsStatOnline
from core.choices import ONLINE_TYPE_CHOICES, METRIC_CHOICES
from utils.person_filter import ListFilter


class OnlineFilter(django_filters.rest_framework.FilterSet):
    """
    所有实时工作数据的通用过滤类
    """
    type = django_filters.ChoiceFilter(method='type_filter', help_text='标准类型',
                                       choices=ONLINE_TYPE_CHOICES, required=True,
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

    def type_filter(self, queryset, name, value):
        self.Meta.model = globals()[f"Dms{value.title()}Online"]  # 动态指定model
        return queryset

    def id_filter(self, queryset, name, value):
        sms_type = self.request.query_params["type"]
        # 先过滤出实时数据(24小时内)
        one_day_ago = datetime.now() - timedelta(hours=24, minutes=0, seconds=0)
        queryset = queryset.filter(time__gte=one_day_ago)
        if sms_type == "dpt":
            return queryset
        return queryset.filter(**{f'{sms_type}_id': value})

    def metric_filter(self, queryset, name, value):
        # 交给Serializer来过滤字段
        return queryset  # such as s_efficiency

    class Meta:
        fields = ['type', 'id', 'metric']


