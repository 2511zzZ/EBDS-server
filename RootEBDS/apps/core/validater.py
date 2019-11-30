# coding: utf-8
"""
借鉴自https://docs.djangoproject.com/en/2.1/ref/validators/
"""
from django.core.exceptions import ValidationError
from django.conf import settings


def validate_image(obj):
    img_size = obj.size
    # 限制图片上传的大小
    if img_size > settings.MAX_FILE_SIZE:
        raise ValidationError('上传文件超过了{}MB！'.format((settings.MAX_FILE_SIZE / (1024 * 1024))))
