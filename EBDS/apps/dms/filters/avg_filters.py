# coding: utf-8
import django_filters
from rest_framework.exceptions import ValidationError

from ..models import DmsTeamAvg, DmsGroupAvg, DmsWorkshopAvg, DmsDptAvg, DmsStatAvg
from core.choices import AVERAGE_TYPE_CHOICES, METRIC_CHOICES
from utils.person_filter import ListFilter


class AverageFilter(django_filters.rest_framework.FilterSet):
    """
    所有实时平均工作数据的通用过滤类
    """
    type = django_filters.ChoiceFilter(method='type_filter', field_name='type',
                                       help_text='标准类型', choices=AVERAGE_TYPE_CHOICES, required=True,
                                       error_messages={
                                          "required": "参数缺失!",
                                       }
                                       )
    id = ListFilter(method='id_filter', field_name='id',
                    required=True, error_messages={
                         "required": "参数缺失!",
                    }
                    )
    metric = django_filters.ChoiceFilter(method='metric_filter', choices=METRIC_CHOICES)

    def type_filter(self, queryset, name, value):
        self.Meta.model = globals()[f"Dms{value.title()}Avg"]  # 动态指定model
        return queryset

    def id_filter(self, queryset, name, value):
        sms_type = self.request.query_params["type"]
        if sms_type == "dpt":
            return queryset
        try:
            value = list(filter(None, value.split(",")))
            # such as team_id__in=value
            return queryset.filter(**{"__".join([f'{sms_type}_id', 'in']): value})
        except Exception:
            error_msg = {"invalid": "请检查字段信息!"}
            msg = {"id": error_msg["invalid"]}
            raise ValidationError(msg, code='invalid')

    def metric_filter(self, queryset, name, value):
        # 交给Serializer来过滤字段
        return queryset   # such as s_efficiency

    class Meta:
        fields = ['type', 'id', 'metric']


