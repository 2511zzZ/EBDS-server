# coding: utf-8
import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import AmsBaseInfo, AmsConveyInfo
from utils.redis_tools import RedisClient
from core import name_map


class AmsBaseInfoSerializer(serializers.ModelSerializer):

    # 用于更新request.user的AmsConveyInfo表中is_delete字段
    is_delete = serializers.BooleanField(write_only=True)

    class Meta:
        model = AmsBaseInfo
        fields = "__all__"
        # 只允许更新is_delete和status
        read_only_fields = ['alert_id', 'stat_id', 'employee_id', 'employee_name',
                            'reason', 'start_time', 'end_time', 'final_deal_employee_id',
                            'final_deal_employee_name', 'deal_role_id']
        # extra_kwargs = {'is_delete': {'write_only': True}}

    def validate_is_delete(self, is_delete):
        """更新is_delete的验证逻辑:前提status!=1"""
        if self.instance.status == 1:
            raise serializers.ValidationError("警报处于待处理状态，无法删除")
        return is_delete

    def validate_status(self, status):
        """标记该alert为已处理的验证逻辑:前提status==1, 并且需要put status=2"""
        if status != 2:
            raise serializers.ValidationError("错误的请求值")
        if self.instance.status != 1:
            raise serializers.ValidationError("该警报已被处理")
        return status

    def update(self, instance, validated_data):
        # 如果是修改status，需要更新额外信息
        user = self.context["request"].user
        if "status" in validated_data:
            instance.end_time = datetime.datetime.now()
            instance.final_deal_employee_id = user.employee_id
            instance.final_deal_employee_name = user.employee.name
            instance.deal_role_id = user.employee.type
            instance.status = validated_data["status"]

        if "is_delete" in validated_data:
            convey_instance = instance.alert_convey_info.get(
                deal_employee_id=user.employee_id
            )
            convey_instance.is_delete = validated_data["is_delete"]
            convey_instance.save()

        instance.save()
        return instance


class AmsDetailInfoSerializer(serializers.ModelSerializer):
    """警报详细信息序列化器"""
    alert = AmsBaseInfoSerializer()  # 警报基本信息
    alert_id = serializers.SerializerMethodField()  # 警报id
    timeout_duration = serializers.SerializerMethodField()  # 超时时间
    title = serializers.SerializerMethodField()  # 效率未达标/工位缺人
    description = serializers.SerializerMethodField()  # 详细描述

    class Meta:
        model = AmsConveyInfo
        fields = ('alert_id', 'alert', 'is_timeout', 'timeout_duration', 'time', 'title', 'description')

    def get_alert_id(self, obj):
        return obj.alert.alert_id

    def get_timeout_duration(self, obj):
        if obj.alert.status != 1 or not obj.is_timeout:  # 只有待处理中的警报才考虑超时时间
            return ""
        transfer_minutes = RedisClient.cfg_alert_transfer_conf()["timeout"]

        # 获取当前时间与time的差值 - transfer_minutes
        start_time = datetime.datetime.strptime(str(obj.time).split('.')[0], "%Y-%m-%d %H:%M:%S")
        current_time = datetime.datetime.now()
        timeout_seconds = (current_time - start_time).seconds
        timeout_seconds = timeout_seconds - transfer_minutes*60
        # 未满一分钟算成1分钟
        return "{hours}:{minutes}".format(hours=timeout_seconds // 3600,
                                          minutes=(timeout_seconds // 60) % 60 + 1)

    def get_title(self, obj):
        alert_reason = obj.alert.reason
        if "效率" in alert_reason:
            return "效率未达标" + "-" + str(obj.alert.alert_id)
        elif "缺人" in alert_reason:
            return "工位缺人" + "-" + str(obj.alert.alert_id)

    def get_description(self, obj):
        return "{stat_id}号工位{employee_id}号员工{employee_name}{reason}，开始时间：{start_time}".format(
            stat_id=obj.alert.stat_id, employee_id=obj.alert.employee_id,
            employee_name=obj.alert.employee_name, reason=obj.alert.reason,
            start_time=obj.alert.start_time
        )


class AmsOverviewSerializer(serializers.Serializer):
    """警报总览信息序列化器"""
    to_do_counts = serializers.SerializerMethodField()  # 待办的警报数
    completed_alerts_this_month = serializers.SerializerMethodField()  # 当月处理的警报数
    avg_process_duration_this_month = serializers.SerializerMethodField()  # 当月警报平均处理时间

    class Meta:
        fields = ('to_do_counts', 'completed_alerts_this_month',
                  'avg_process_duration_this_month')

    def get_to_do_counts(self, user):
        if user.is_superuser:
            return 0
        return AmsConveyInfo.objects.filter(deal_employee_id=user.employee_id,
                                            alert__status=1).count()

    def get_completed_alerts_this_month(self, user):
        if user.is_superuser:
            return 0
        return AmsConveyInfo.objects.filter(deal_employee_id=user.employee_id,
                                            time__gte=datetime.date.today().replace(day=1),
                                            alert__final_deal_employee_id=user.employee_id).count()

    def get_avg_process_duration_this_month(self, user):
        if user.is_superuser:
            return "暂无"
        all_solve_alerts = AmsConveyInfo.objects.filter(
            deal_employee_id=user.employee_id,
            time__gte=datetime.date.today().replace(day=1),
            alert__final_deal_employee_id=user.employee_id,
            alert__status=2
            )
        if not all_solve_alerts:
            return "暂无"
        # 计算警报平均处理时间
        process_duration = datetime.timedelta(seconds=0)
        for obj in all_solve_alerts:
            process_duration += obj.alert.solve_seconds
        return str(process_duration / all_solve_alerts.count()).split(".")[0]  # 不返回毫秒


class AmsTransferSerializer(serializers.Serializer):
    """警报传递信息序列化器"""
    status = serializers.SerializerMethodField()  # 警报状态
    transfer_way = serializers.SerializerMethodField()  # 警报传递的整个路径

    class Meta:
        fields = ('status', 'transfer_way')

    def get_status(self, obj):
        return obj.status

    def get_transfer_way(self, obj):
        way = []
        for step in obj.alert_convey_info.all():
            role_id = step.role_id
            role_name = name_map.ROLE_MAP[step.role_id]
            deal_employee_name = step.deal_employee_name
            deal_employee_id = step.deal_employee_id
            time = step.time
            way.append({"tip": "接收警报",
                        "role_id": role_id, "role_name": role_name,
                        "deal_employee_name": deal_employee_name,
                        "deal_employee_id": deal_employee_id,
                        "time": time})
        if obj.status == 1:  # 待处理
            way.append({"tip": "待处理"})
        elif obj.status == 2:  # 已处理
            final_deal_employee_id = obj.final_deal_employee_id
            final_deal_employee_name = obj.final_deal_employee_id
            role_id = obj.deal_role_id
            role_name = name_map.ROLE_MAP[obj.deal_role_id]
            end_time = obj.end_time
            way.append({"tip": "已处理", "role_id": role_id, "role_name": role_name,
                        "final_deal_employee_id": final_deal_employee_id,
                        "final_deal_employee_name": final_deal_employee_name,
                        "end_time": end_time})
        elif obj.status in (-1, 3):  # 已关闭
            way.append({"tip": "已关闭", "end_time": obj.end_time})

        return way
