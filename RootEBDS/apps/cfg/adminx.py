# coding: utf-8
import xadmin
from .models import CfgAlertCondition, CfgAlertTransfer, CfgBaseInquiry, \
    CfgUserInquiry, CfgWorkPeriod


class CfgAlertConditionAdmin(object):
    list_display = ['duration', 'percent']


class CfgAlertTransferAdmin(object):
    list_display = ['timeout', 'max_timeout']


class CfgBaseInquiryAdmin(object):
    list_display = ['id', 'name', 'description']
    list_filter = list_display


class CfgUserInquiryAdmin(object):
    list_display = ['employee', 'cfg', 'status', 'value']
    search_fields = ['employee']
    list_filter = list_display


class CfgWorkPeriodAdmin(object):
    list_display = ['name', 'start_time', 'end_time']


xadmin.site.register(CfgAlertCondition, CfgAlertConditionAdmin)
xadmin.site.register(CfgAlertTransfer, CfgAlertTransferAdmin)
xadmin.site.register(CfgBaseInquiry, CfgBaseInquiryAdmin)
xadmin.site.register(CfgUserInquiry, CfgUserInquiryAdmin)
xadmin.site.register(CfgWorkPeriod, CfgWorkPeriodAdmin)
