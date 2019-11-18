# coding: utf-8

import os
import random

from django.db import IntegrityError
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EBDS.EBDS.settings")  # 因为Django工程位于第二级

import django
django.setup()

from django.contrib.auth import get_user_model
from sms.models import Member
User = get_user_model()

from xpinyin import Pinyin

pinyin = Pinyin()
# print(pinyin.get_pinyin("钓鱼岛是中国的", ""))


def insert_to_db(default_password='123456'):
    for member in Member.objects.filter(type__in=[2, 3, 4]):  # 除工人之外的员工
        try:
            user = User()
            user.username = pinyin.get_pinyin(member.name, "")
            user.set_password(default_password)
            user.nickname = member.name
            user.employee_id = member.employee_id
            user.save()
        except IntegrityError as e:  # username可能重名
            # 重新生成username
            related_username = User.objects.filter(username__startswith=user.username).order_by('-username')[0]
            user.username = related_username.username + str(random.randint(0, 9))
            user.save()


run = insert_to_db

if __name__ == '__main__':
    insert_to_db()




