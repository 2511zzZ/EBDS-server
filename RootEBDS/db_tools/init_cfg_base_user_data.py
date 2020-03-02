import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RootEBDS.EBDS.settings")
django.setup()

from users.models import User
from cfg.models import CfgBaseInquiry, CfgUserInquiry

CfgBaseInquiry.objects.all().delete()
CfgUserInquiry.objects.all().delete()
CfgBaseInquiry.objects.create(id=1, name="默认查询时间间隔", mode=1, description="默认查询时间间隔")
user_query_set = User.objects.all()
for one_user_obj in user_query_set:
    CfgUserInquiry.objects.create(value=10, status=None, cfg_id=1, user_id=one_user_obj.id)
