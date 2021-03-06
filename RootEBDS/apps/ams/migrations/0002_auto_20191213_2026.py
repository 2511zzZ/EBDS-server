# Generated by Django 2.1.11 on 2019-12-13 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ams', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amsbaseinfo',
            name='deal_role_id',
            field=models.IntegerField(blank=True, choices=[(2, '大组长'), (3, '经理'), (4, '总经理')], null=True, verbose_name='最终处理人角色类别'),
        ),
        migrations.AlterField(
            model_name='amsbaseinfo',
            name='status',
            field=models.IntegerField(blank=True, choices=[(-1, '异常警报'), (1, '待处理'), (2, '已处理'), (3, '已关闭')], null=True, verbose_name='警报状态'),
        ),
        migrations.AlterField(
            model_name='amsconveyinfo',
            name='deal_employee_id',
            field=models.IntegerField(default=1, verbose_name='处理人员工号'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='amsconveyinfo',
            name='deal_employee_name',
            field=models.CharField(default='1', max_length=255, verbose_name='处理人姓名'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='amsconveyinfo',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AlterField(
            model_name='amsconveyinfo',
            name='is_timeout',
            field=models.BooleanField(default=False, verbose_name='是否超时'),
        ),
        migrations.AlterField(
            model_name='amsconveyinfo',
            name='role_id',
            field=models.IntegerField(choices=[(2, '大组长'), (3, '经理'), (4, '总经理')], default=2, verbose_name='处理人角色类别'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='amsconveyinfo',
            name='time',
            field=models.DateTimeField(default='2019-10-10 10:00:00', verbose_name='收到警报的时间'),
            preserve_default=False,
        ),
    ]
