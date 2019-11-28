# coding: utf-8

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    real_name = serializers.ReadOnlyField(source='employee.name')  # 真实姓名
    sex = serializers.ReadOnlyField(source='employee.sex')  # 性别
    birthday = serializers.ReadOnlyField(source='employee.birthday')  # 生日
    birthplace = serializers.ReadOnlyField(source='employee.birthplace')  # 所在地
    role = serializers.SerializerMethodField()  # 角色类别
    level = serializers.SerializerMethodField()  # 管理层级:group/workshop/dpt
    level_id = serializers.SerializerMethodField()  # 管理层级id
    
    class Meta:
        model = User
        fields = ('username', 'employee', 'real_name', 'nickname', 'icon',
                  'sex', 'birthday', 'birthplace', 'role', 'level', 'level_id')

    def get_role(self, obj):
        if obj.is_superuser:
            return 4
        return obj.employee.type

    def get_level(self, obj):
        if obj.is_superuser:
            return 'dpt'
        role_level_dict = {4: 'dpt', 3: 'workshop', 2: 'group'}
        return role_level_dict[obj.employee.type]

    def get_level_id(self, obj):
        if obj.is_superuser or obj.employee.type == 4:
            return 1
        role_level_id_dict = {3: 'workshop', 2: 'group'}
        level_name = role_level_id_dict[obj.employee.type]
        # 反向查询
        return getattr(obj.employee, f'employee_{level_name}').all()[0].id
