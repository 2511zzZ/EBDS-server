# coding: utf-8
from django.db import models


class DmsActionInfo(models.Model):
    """
    基本动作时间信息
    """
    id = models.IntegerField(primary_key=True)
    action_id = models.IntegerField()
    stat_id = models.IntegerField(blank=True, null=True)
    spend_sec = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        # TODO:后期完善
        managed = False
        db_table = 'dms_action_info'
