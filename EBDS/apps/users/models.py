from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from sms.models import Member


class User(AbstractUser):
    """
    用户
    """
    employee = models.ForeignKey(Member, related_name="user_info",
                                 verbose_name='员工号', null=True,
                                 on_delete=models.CASCADE, db_constraint=False)
    nickname = models.CharField(max_length=64, verbose_name="姓名", null=True)
    icon = models.ImageField(max_length=500, verbose_name='头像', upload_to="head_photo/",
                             default="head_photo/default.jpg", blank=True, null=True)

    class Meta:
        db_table = 'auth_user'
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
