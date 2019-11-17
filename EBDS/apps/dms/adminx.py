# coding: utf-8
import xadmin
from .models import DmsTeamAvg, DmsGroupAvg, DmsWorkshopAvg, DmsDptAvg, DmsStatAvg
from .models import DmsTeamDaily, DmsGroupDaily, DmsWorkshopDaily, DmsDptDaily, DmsStatDaily, DmsWorkerDaily
from .models import DmsTeamOnline, DmsGroupOnline, DmsWorkshopOnline, DmsDptOnline, DmsStatOnline
from .models import DmsActionInfo


class DmsTeamDailyAdmin(object):
    list_display = ['team_id', 'efficiency', 'accuracy', 'workhour', 'time']
    search_fields = ['team_id', ]
    list_filter = ['time']


class DmsGroupDailyAdmin(object):
    list_display = ['group_id', 'efficiency', 'accuracy', 'workhour', 'time']
    search_fields = ['group_id', ]
    list_filter = ['time']


class DmsWorkshopAdmin(object):
    list_display = ['workshop_id', 'efficiency', 'accuracy', 'workhour', 'time']
    search_fields = ['workshop_id', ]
    list_filter = ['time']


class DmsDptDailyAdmin(object):
    list_display = ['efficiency', 'accuracy', 'workhour', 'time']
    list_filter = ['time']


class DmsStatDailyAdmin(object):
    list_display = ['stat_id', 'efficiency', 'accuracy', 'workhour', 'time']
    search_fields = ['stat_id', ]
    list_filter = ['time']


class DmsWorkerDailyAdmin(object):
    list_display = ['employee_id', 'efficiency', 'accuracy', 'workhour', 'time']
    search_fields = ['employee_id', ]
    list_filter = ['time']


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class DmsTeamOnlineAdmin(object):
    list_display = ['team_id', 'efficiency', 'accuracy', 'workhour', 'time']
    search_fields = ['team_id', ]
    list_filter = ['time']


class DmsGroupOnlineAdmin(object):
    list_display = ['group_id', 'efficiency', 'accuracy', 'workhour', 'time']
    search_fields = ['group_id', ]
    list_filter = ['time']


class DmsWorkshopOnlineAdmin(object):
    list_display = ['workshop_id', 'efficiency', 'accuracy', 'workhour', 'time']
    search_fields = ['workshop_id', ]
    list_filter = ['time']


class DmsDptOnlineAdmin(object):
    list_display = ['efficiency', 'accuracy', 'workhour', 'time']
    list_filter = ['time']


class DmsStatOnlineAdmin(object):
    list_display = ['stat_id', 'efficiency', 'accuracy', 'workhour', 'time']
    search_fields = ['stat_id', ]
    list_filter = ['time']


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class DmsTeamAvgAdmin(object):
    list_display = ['team_id', 'a_efficiency', 'a_accuracy', 'a_workhour', 'time']
    search_fields = ['team_id', ]
    list_filter = ['time']


class DmsGroupAvgAdmin(object):
    list_display = ['group_id', 'a_efficiency', 'a_accuracy', 'a_workhour', 'time']
    search_fields = ['group_id', ]
    list_filter = ['time']


class DmsWorkshopAvgAdmin(object):
    list_display = ['workshop_id', 'a_efficiency', 'a_accuracy', 'a_workhour', 'time']
    search_fields = ['workshop_id', ]
    list_filter = ['time']


class DmsDptAvgAdmin(object):
    list_display = ['a_efficiency', 'a_accuracy', 'a_workhour', 'time']
    list_filter = ['time']


class DmsStatAvgAdmin(object):
    list_display = ['stat_id', 'a_efficiency', 'a_accuracy', 'a_workhour', 'time']
    search_fields = ['stat_id', ]
    list_filter = ['time']


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class DmsActionInfoAdmin(object):
    # TODO:后期完善
    pass


xadmin.site.register(DmsTeamDaily, DmsTeamDailyAdmin)
xadmin.site.register(DmsGroupDaily, DmsGroupDailyAdmin)
xadmin.site.register(DmsWorkshopDaily, DmsWorkshopAdmin)
xadmin.site.register(DmsDptDaily, DmsDptDailyAdmin)
xadmin.site.register(DmsStatDaily, DmsStatDailyAdmin)
xadmin.site.register(DmsWorkerDaily, DmsWorkerDailyAdmin)

xadmin.site.register(DmsTeamOnline, DmsTeamOnlineAdmin)
xadmin.site.register(DmsGroupOnline, DmsGroupOnlineAdmin)
xadmin.site.register(DmsWorkshopOnline, DmsWorkshopOnlineAdmin)
xadmin.site.register(DmsDptOnline, DmsDptOnlineAdmin)
xadmin.site.register(DmsStatOnline, DmsStatOnlineAdmin)

xadmin.site.register(DmsTeamAvg, DmsTeamAvgAdmin)
xadmin.site.register(DmsGroupAvg, DmsGroupAvgAdmin)
xadmin.site.register(DmsWorkshopAvg, DmsWorkshopAvgAdmin)
xadmin.site.register(DmsDptAvg, DmsDptAvgAdmin)
xadmin.site.register(DmsStatAvg, DmsStatAvgAdmin)

# xadmin.site.register(DmsActionInfo, DmsActionInfoAdmin)
