# coding: utf-8
"""
自定义Serializer基类
"""
from rest_framework import serializers
from collections import OrderedDict


class StandardSerializer(serializers.ModelSerializer):
    """
    Standard 根据metric返回指定字段
    """

    def get_fields(self):
        fields = super().get_fields()
        pk_name = self.Meta.model._meta.pk.name
        metric = self.context['request'].query_params.get('metric')  # 获取路径参数
        if metric and metric in ('efficiency', 'accuracy', 'workhour'):
            return OrderedDict([(pk_name, fields[pk_name]),
                                ("s_" + metric, fields["s_" + metric])])
        return fields


