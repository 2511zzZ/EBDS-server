# coding: utf-8
import xadmin
from .models import AmsBaseInfo, AmsConveyInfo


class AmsBaseInfoAdmin(object):
    list_display = ['alert_id', 'stat_id', 'employee_id', 'employee_name',
                    'reason', 'start_time', 'end_time', 'final_deal_employee_id',
                    'final_deal_employee_name', 'deal_role_id', 'status']
    search_fields = ['alert_id', 'stat_id', ]
    list_filter = ['alert_id', 'stat_id', 'employee_id', 'employee_name',
                   'reason', 'start_time', 'end_time', 'final_deal_employee_id',
                   'final_deal_employee_name', 'deal_role_id', 'status']


class AmsConveyInfoAdmin(object):
    list_display = ['alert', 'deal_employee_id', 'deal_employee_name', 'role_id', 'is_timeout', 'is_delete', 'time']
    search_fields = ['alert', ]
    list_filter = ['alert', 'deal_employee_id', 'deal_employee_name', 'role_id', 'is_timeout', 'is_delete', 'time']


xadmin.site.register(AmsBaseInfo, AmsBaseInfoAdmin)
xadmin.site.register(AmsConveyInfo, AmsConveyInfoAdmin)
