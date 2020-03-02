from collections import OrderedDict

from rest_framework import serializers
from .models import CfgBaseInquiry, CfgUserInquiry
from .models import CfgAlertCondition, CfgAlertTransfer


class BaseInquirySerializer(serializers.ModelSerializer):
    mode = serializers.IntegerField(min_value=1)

    class Meta:
        model = CfgBaseInquiry
        fields = "__all__"


class UserInquirySerializer(serializers.ModelSerializer):
    scope = {
        "value_scope": [0, 60],
        "status_scope": [0, 1]
    }

    class Meta:
        model = CfgUserInquiry
        fields = ("cfg", "status", "value")
        read_only_fields = ["cfg", "mode"]

    def __switch_cfg_mode__(self, response, cfg):
        """
        根据cfg选择提供设置方式
        :param response:
        :param cfg: BaseInquiry对象
        :return: 筛选后的response
        """
        # 1只能设置value, 2只能设置status
        if cfg.mode == 1:
            response.pop("status")
        if cfg.mode == 2:
            response.pop("value")

        return response

    def __get_pretty_response__(self, response):
        """
        通过字典的形式嵌套原有的response, 以提供带有详细描述的接口数据
        :param response:
        :param cfg:
        :return:
        """
        for key in response.keys():
            if key != "cfg":
                response[key] = {"value": response[key],
                                 "scope": self.scope[key + "_scope"]}
        return response

    def to_representation(self, instance):
        print(instance.status)
        response = self.__switch_cfg_mode__(super().to_representation(instance), instance.cfg)
        pretty_response = self.__get_pretty_response__(response)

        return pretty_response

    def validate_status(self, status):
        if self.instance is None:
            raise serializers.ValidationError("应该先添加用户设置")
        if self.instance.cfg.mode != 2:
            raise serializers.ValidationError(self.instance.cfg.name + "不支持开关")
        return status

    def validate_value(self, value):
        if self.instance is None:
            raise serializers.ValidationError("应该先添加用户设置")
        cur_instance_cfg = self.instance.cfg
        if cur_instance_cfg.id == 1:
            if value <= 0:
                raise serializers.ValidationError(
                    cur_instance_cfg.name + ":不能小于或等于0")
            if value > 60:
                raise serializers.ValidationError(
                    cur_instance_cfg.name + ":不能大于60")
        else:
            raise serializers.ValidationError("当前mode不支持value")
        return value


class CfgAlertConditionSerializer(serializers.ModelSerializer):

    duration_scope = [0, 60]
    percent_scope = [0.00, 1.00]

    class Meta:
        model = CfgAlertCondition
        fields = ('duration', 'percent')

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response["duration"] = {"value": response["duration"],
                                "scope": [self.duration_scope[0], self.duration_scope[1]]}

        response["percent"] = {"value": float(response["percent"]),
                               "scope": [self.percent_scope[0], self.percent_scope[1]]}

        return response

    def validate_duration(self, duration):
        """范围1-60(单位:minutes)"""
        if duration > self.duration_scope[1] or duration < self.duration_scope[0]:
            raise serializers.ValidationError(f"范围需要在{self.duration_scope[0]}-"
                                              f"{self.duration_scope[1]}之间")
        return duration

    def validate_percent(self, percent):
        """范围0-1的小数"""
        if percent > self.percent_scope[1] or percent < self.percent_scope[0]:
            raise serializers.ValidationError(f"范围需要在{self.percent_scope[0]*100}%-"
                                              f"{self.percent_scope[1]*100}%之间")

        return percent


class CfgAlertTransferSerializer(serializers.ModelSerializer):
    timeout_scope = [1, 60]
    max_timeout_scope = [3, 1440]

    class Meta:
        model = CfgAlertTransfer
        fields = ("timeout", "max_timeout")

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response["timeout"] = {"value": response["timeout"],
                               "scope": [self.timeout_scope[0], self.timeout_scope[1]]}

        response["max_timeout"] = {"value": response["max_timeout"],
                                   "scope": [self.max_timeout_scope[0],
                                             self.max_timeout_scope[1]]}
        return response

    def validate_timeout(self, timeout):
        """范围1-60(单位:minutes)"""
        if timeout > self.timeout_scope[1] or timeout < self.timeout_scope[0]:
            raise serializers.ValidationError(f"范围需要在{self.timeout_scope[0]}-"
                                              f"{self.timeout_scope[1]}之间")
        return timeout

    def validate_max_timeout(self, max_timeout):
        """范围3*timeout-1440(单位:minutes)"""
        post_kv = self.context['request'].POST
        if "timeout" in post_kv:  # 如果用户post两个值的处理
            max_timeout_scope_min = 3 * int(post_kv["timeout"])
        else:
            max_timeout_scope_min = 3 * self.instance.timeout
        if max_timeout > self.max_timeout_scope[1] or max_timeout < max_timeout_scope_min:
            raise serializers.ValidationError(f"范围需要在3倍的timeout-"
                                              f"{self.max_timeout_scope[1]}之间")
        return max_timeout

