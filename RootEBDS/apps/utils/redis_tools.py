# coding: utf-8
import decimal
import redis
from django.conf import settings
from cfg.models import CfgAlertCondition, CfgAlertTransfer


class RedisClient:
    def __init__(self, url=settings.REDIS_URL):
        self._redis = redis.from_url(url=url)

    # 保证单例，减少连接数
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance'):
            cls.__instance = object.__new__(cls)
        return cls.__instance

    @property
    def redis(self):
        return self._redis

    @staticmethod
    def cfg_alert_transfer_conf():
        _redis = RedisClient().redis
        timeout = _redis.get("timeout")
        max_timeout = _redis.get("max_timeout")

        if (timeout is None) or (max_timeout is None):
            try:
                timeout = CfgAlertTransfer.objects.all()[0].timeout
                max_timeout = CfgAlertTransfer.objects.all()[0].max_timeout
            except IndexError:
                print("========================")
                print("数据表CfgAlertTransfer可能是没有数据")
            _redis.mset({"timeout": timeout, "max_timeout": max_timeout})
        return {"timeout": int(timeout), "max_timeout": int(max_timeout)}

    @staticmethod
    def cfg_alert_condition_conf():
        _redis = RedisClient().redis
        duration = _redis.get("duration")
        percent = _redis.get("percent")

        if (duration is None) or (percent is None):
            try:
                duration = CfgAlertCondition.objects.all()[0].duration
                percent = CfgAlertCondition.objects.all()[0].percent
            except IndexError:
                print("=========redis_tools=========")
                print("CfgAlertCondition可能没有数据")
            _redis.mset({"duration": duration, "percent": float(percent)})

        return {"duration": int(duration), "percent": decimal.Decimal(float(percent))}
