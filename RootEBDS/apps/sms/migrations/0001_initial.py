# Generated by Django 2.2.7 on 2019-11-20 21:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False, verbose_name='员工号')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='姓名')),
                ('sex', models.CharField(blank=True, choices=[('male', '男'), ('female', '女')], max_length=255, null=True, verbose_name='性别')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='出生日期')),
                ('birthplace', models.CharField(blank=True, max_length=255, null=True, verbose_name='所在地')),
                ('type', models.IntegerField(blank=True, choices=[(1, '工人'), (2, '大组长'), (3, '经理'), (4, '总经理')], null=True, verbose_name='员工类别')),
            ],
            options={
                'verbose_name': '公司成员',
                'verbose_name_plural': '公司成员',
                'db_table': 'sms_member',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='小组号')),
                ('name', models.CharField(max_length=255, verbose_name='小组名')),
            ],
            options={
                'verbose_name': '小组信息',
                'verbose_name_plural': '小组信息',
                'db_table': 'sms_team',
            },
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='车间号')),
                ('name', models.CharField(max_length=255, verbose_name='车间名')),
                ('employee', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_workshop', to='sms.Member', verbose_name='车间管理员工号')),
            ],
            options={
                'verbose_name': '车间信息',
                'verbose_name_plural': '车间信息',
                'db_table': 'sms_workshop',
            },
        ),
        migrations.CreateModel(
            name='TeamStatMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stat_id', models.IntegerField(verbose_name='工位号')),
                ('morning_shift_id', models.IntegerField(blank=True, null=True, verbose_name='早班员工号')),
                ('middle_shift_id', models.IntegerField(blank=True, null=True, verbose_name='中班员工号')),
                ('night_shift_id', models.IntegerField(blank=True, null=True, verbose_name='晚班员工号')),
                ('update_time', models.DateField(blank=True, default=datetime.datetime.now, null=True, verbose_name='记录时间')),
                ('team', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='team_stat_member', to='sms.Team', verbose_name='小组号')),
            ],
            options={
                'verbose_name': '小组工人排班表',
                'verbose_name_plural': '小组工人排班表',
                'db_table': 'sms_team_stat_member',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='大组号')),
                ('name', models.CharField(max_length=255, verbose_name='大组名')),
                ('employee', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_group', to='sms.Member', verbose_name='大组管理员工号')),
            ],
            options={
                'verbose_name': '大组信息',
                'verbose_name_plural': '大组信息',
                'db_table': 'sms_group',
            },
        ),
        migrations.CreateModel(
            name='Dpt',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='生产部号')),
                ('name', models.CharField(max_length=255, verbose_name='生产部名')),
                ('employee', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='sms.Member', verbose_name='生产部管理员工号')),
            ],
            options={
                'verbose_name': '生产部信息',
                'verbose_name_plural': '生产部信息',
                'db_table': 'sms_dpt',
            },
        ),
        migrations.CreateModel(
            name='TeamGroupWorkshop',
            fields=[
                ('team', models.OneToOneField(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='level_relate', serialize=False, to='sms.Team', verbose_name='小组号')),
                ('group', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='level_relate', to='sms.Group', verbose_name='大组号')),
                ('workshop', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='level_relate', to='sms.Workshop', verbose_name='车间号')),
            ],
            options={
                'verbose_name': '小组-大组-车间层级关系',
                'verbose_name_plural': '小组-大组-车间层级关系',
                'db_table': 'sms_team_group_workshop',
            },
        ),
    ]