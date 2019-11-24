# coding: utf-8
"""
自定义Serializer基类
"""
from rest_framework import serializers
from collections import OrderedDict
from sms.models import TeamStatMember, Member
from cfg.models import CfgWorkPeriod


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


# Daily 根据metric返回指定字段
DailySerializer = OnlineSerializer


class DmsListSerializer(serializers.ListSerializer):
    """
    Online & Daily 数据的序列化格式公共抽象类
    """
    def to_representation(self, data) -> list:
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


class OnlineListSerializer(DmsListSerializer):
    """
    重写Online序列化格式
    """
    def to_representation(self, data):
        response = super().to_representation(data)
        metric = self.context['request'].query_params.get('metric')  # 获取路径参数
        sms_type = self.context['request'].query_params.get('type')
        req_id = self.context['request'].query_params.get('id')
        if sms_type == 'stat':
            # 获取worker+period信息
            worker_list = []
            stat_obj = TeamStatMember.objects.filter(stat_id=req_id).order_by('-update_time')[0]
            for period in CfgWorkPeriod.objects.all():
                worker_dict = OrderedDict()
                worker_dict['worker_id'] = getattr(stat_obj, f"{period.name}_shift_id")
                worker_dict['name'] = Member.objects.get(employee_id=worker_dict['worker_id']).name
                worker_dict['period'] = [period.start_time, period.end_time]
                worker_list.append(worker_dict)

            # 更新response
            response[0]['worker'] = worker_list
            response[0].move_to_end(metric)
        return response

