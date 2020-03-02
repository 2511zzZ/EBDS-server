# coding: utf-8
import django_filters
from django.db.models import Q, Max

from .models import AmsConveyInfo
from core.choices import ALERT_STATUS_FOR_FILTER


class AlertDetailFilter(django_filters.rest_framework.FilterSet):

    status = django_filters.ChoiceFilter(method='status_filter', help_text='警报状态',
                                         choices=ALERT_STATUS_FOR_FILTER, required=True,
                                         error_messages={
                                           "required": "参数缺失!",
                                         }
                                         )

    def status_filter(self, queryset, name, value):
        if value == 3:
            return queryset.filter(alert__status__in=(-1, 3))
        return queryset.filter(alert__status=value, is_delete=False)

    class Meta:
        # model = AmsConveyInfo
        fields = ['status']
