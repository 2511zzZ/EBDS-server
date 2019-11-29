# coding: utf-8
from django.core.files.storage import FileSystemStorage
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.conf import settings

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
        fields = ('username', 'employee', 'real_name', 'nickname', 'sex',
                  'birthday', 'birthplace', 'role', 'level', 'level_id', 'icon')
        # 只允许更新nickname和icon
        read_only_fields = ['username', 'employee', 'real_name', 'sex',
                            'birthday', 'birthplace', 'role', 'level', 'level_id']

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


class AvatarSerializer(serializers.Serializer):
    avatar = serializers.ImageField(write_only=True, max_length=500, help_text='头像')

    class Meta:
        fields = ('avatar',)

    def create(self, validated_data):
        img_size = validated_data['avatar'].size
        # 限制图片上传的大小
        if img_size > settings.MAX_FILE_SIZE:
            return {'error': '上传文件超过了{}MB！'.format((settings.MAX_FILE_SIZE / (1024 * 1024)))}
        name = validated_data['avatar'].name
        content = validated_data['avatar']
        # 重编码图片名
        file_handle = FileSystemStorage(location=settings.MEDIA_ROOT+'/head_photo/',
                                        base_url=settings.MEDIA_URL+'/head_photo/')
        # 返回新的图片名
        img_name = file_handle.save(name, content)
        return {'size': img_size,
                'img_url': self.context['request']._current_scheme_host + file_handle.url(img_name)}



