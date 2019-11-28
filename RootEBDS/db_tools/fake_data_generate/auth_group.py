# coding: utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RootEBDS.EBDS.settings")  # 因为Django工程位于第二级

import django
django.setup()

from django.contrib.auth.models import Group


def insert_to_db():
    Group.objects.create(id=1, name="工人")
    Group.objects.create(id=2, name="大组长")
    Group.objects.create(id=3, name="经理")
    Group.objects.create(id=4, name="总经理")


run = insert_to_db

if __name__ == '__main__':
    insert_to_db()
