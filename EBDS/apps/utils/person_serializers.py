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


class AverageSerializer(serializers.ModelSerializer):
    """
    Avg 根据metric返回指定字段
    """

    def get_fields(self):
        fields = super().get_fields()

        metric = self.context['request'].query_params.get('metric')  # 获取路径参数
        sms_type = self.context['request'].query_params.get('type')

        if metric and metric in ('efficiency', 'accuracy', 'workhour'):
            return OrderedDict([(sms_type+"_id", fields[sms_type+"_id"]),
                                ("a_" + metric, fields["a_" + metric]),
                                ('time', fields['time'])])
        return fields


class OnlineSerializer(serializers.ModelSerializer):
    """
    Online 根据metric返回指定字段
    """

    def get_fields(self):
        fields = super().get_fields()

        metric = self.context['request'].query_params.get('metric')  # 获取路径参数
        sms_type = self.context['request'].query_params.get('type')

        if metric and metric in ('efficiency', 'accuracy', 'workhour'):
            return OrderedDict([(sms_type+"_id", fields[sms_type+"_id"]),
                                (metric, fields[metric]),
                                ('time', fields['time'])])
        return fields


class DmsListSerializer(serializers.ListSerializer):
    """
    重写Online & Daily 数据的序列化格式
    """
    def to_representation(self, data):
        response = super().to_representation(data)
        metric = self.context['request'].query_params.get('metric')  # 获取路径参数
        sms_type = self.context['request'].query_params.get('type')
        req_id = self.context['request'].query_params.get('id')
        if sms_type == 'dpt':
            req_id = 1

        metric_dict = OrderedDict()
        for obj in response:
            metric_dict[obj["time"]] = obj[metric]

        return [OrderedDict([(sms_type+"_id", int(req_id)), (metric, metric_dict)])]



