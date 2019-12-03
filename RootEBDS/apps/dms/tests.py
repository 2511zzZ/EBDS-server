# -*- coding:UTF-8 -*-
from django.test import TestCase
from django.test import client
from rest_framework import response

from dms.models.daily_models import DmsTeamDaily
from users.models import User
from sms.models import Member


# Create your tests here.
class DmsTeamDailyTest(TestCase):
    def setUp(self):
        member = Member.objects.create(employee_id=201603526, name=u"testname", sex="男", type=3)
        # self.user = User.objects.create(employee=member, username="123xiaoming", password=)
        self.user = User()
        self.user.employee = member
        self.user.username = '123xiaoming'
        self.user.set_password("xiaoming")
        self.user.save()

    def test_ming(self):
        user_ming = User.objects.get(employee_id=201603526)
        self.assertEqual(user_ming.nickname, None)
        self.assertEqual(user_ming.employee.sex, "男")
        self.assertEqual(user_ming.employee.type, 3)

    def test_login(self):
        user_ming = User.objects.get(employee_id=201603526)
        result = self.client.post('/api_authlogin/', {'username': user_ming.username, 'password': user_ming.password})
        print(result.content)
        self.assertEqual(result.status_code, 302)   # 重定向到root页面

        # 104-zhouzhou 大组长: 67  管理小组: 335 334 333 332 331
    def test_permission(self):
        cookie = self.client.post('/api_authlogin/', {'username': "zhouzhou", 'password': "123456"}).cookies
        # 缺少参数
        result = self.client.get('/standards/?format=json', {'cookies': cookie})
        self.assertEqual(result.status_code[:1], 4)
        # 错误参数
        result = self.client.get('/standards/?format=json', {'cookies': cookie, type: "23fds"})
        self.assertEqual(result.status_code[:1], 4)
        self.assertContains(result.json()["type"], "选择一个有效的选项")
        # 访问同级别的权限外数据
        result = self.client.get('/standards/?format=json', {'cookies': cookie, type: "group", id: "1"})
        self.assertEqual(result.json()["details"], "您没有执行该操作的权限。")
        # 访问高级别的数据
        result = self.client.get('/standards/?format=json', {'cookies': cookie, type: "dpt", id: "1"})
        self.assertEqual(result.json()["details"], "您没有执行该操作的权限。")
        # 访问权限内的数据
        result = self.client.get('/standards/?format=json', {'cookies': cookie, type: "group", id: "67"})
        self.assertEqual(result.status_code, 200)
        result = self.client.get('/standards/?format=json', {'cookies': cookie, type: "team", id: "335"})
        self.assertEqual(result.status_code, 200)
        result = self.client.get('/standards/?format=json', {'cookies': cookie, type: "stat", id: "3350"})
        self.assertEqual(result.status_code, 200)

