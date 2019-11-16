# coding: utf-8
import xadmin
from .models import StandardTeam, StandardGroup, StandardWorkshop, StandardDpt
# from .models import StandardBasicAction


class StandardTeamAdmin(object):
    list_display = ['team', 's_efficiency', 's_accuracy', 's_workhour']
    search_fields = ['team', ]
    list_filter = ['team', 's_efficiency', 's_accuracy', 's_workhour']
    # style_fields = {"goods_desc": "ueditor"}


class StandardGroupAdmin(object):
    list_display = ['group', 's_efficiency', 's_accuracy', 's_workhour']
    search_fields = ['group', ]
    list_filter = ['group', 's_efficiency', 's_accuracy', 's_workhour']


class StandardWorkshopAdmin(object):
    list_display = ['workshop', 's_efficiency', 's_accuracy', 's_workhour']
    search_fields = ['workshop', ]
    list_filter = ['workshop', 's_efficiency', 's_accuracy', 's_workhour']


class StandardDptAdmin(object):
    list_display = ['s_efficiency', 's_accuracy', 's_workhour']


xadmin.site.register(StandardTeam, StandardTeamAdmin)
xadmin.site.register(StandardGroup, StandardGroupAdmin)
xadmin.site.register(StandardWorkshop, StandardWorkshopAdmin)
xadmin.site.register(StandardDpt, StandardDptAdmin)



