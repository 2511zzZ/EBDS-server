# coding: utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EBDS.EBDS.settings")  # 因为Django工程位于第二级

import django
django.setup()

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from sms.models import Member
User = get_user_model()


def insert_to_db():
    for user in User.objects.all():
        if user.employee_id:
            user_info = Member.objects.get(employee_id=user.employee_id)
            group_id = user_info.type
            user_id = user.id
            user.groups.add(Group.objects.get(id=group_id))


run = insert_to_db

if __name__ == '__main__':
    insert_to_db()

