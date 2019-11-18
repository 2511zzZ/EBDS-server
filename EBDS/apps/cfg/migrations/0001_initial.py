# Generated by Django 2.2.7 on 2019-11-18 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CfgAlertCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField(verbose_name='低于标准效率的持续时间(单位:分钟)')),
                ('percent', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='低于标准效率的百分比(小数表示)')),
            ],
            options={
                'verbose_name': '警报条件参数',
                'verbose_name_plural': '警报条件参数',
                'db_table': 'cfg_alert_condition',
            },
        ),
        migrations.CreateModel(
            name='CfgAlertTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeout', models.IntegerField(verbose_name='超时传递时间(单位:分钟)')),
                ('max_timeout', models.IntegerField(verbose_name='警报最长处理时间(单位:分钟)')),
            ],
            options={
                'verbose_name': '警报传递参数',
                'verbose_name_plural': '警报传递参数',
                'db_table': 'cfg_alert_transfer',
            },
        ),
        migrations.CreateModel(
            name='CfgBaseInquiry',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='配置号')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='配置名')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='详细描述')),
            ],
            options={
                'verbose_name': '「查询设置」配置',
                'verbose_name_plural': '「查询设置」配置',
                'db_table': 'cfg_base_inquiry',
            },
        ),
        migrations.CreateModel(
            name='CfgWorkPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(blank=True, choices=[('morning', '早'), ('middle', '中'), ('night', '晚')], null=True, verbose_name='时间段')),
                ('start_time', models.TimeField(blank=True, null=True, verbose_name='开始时间')),
                ('end_time', models.TimeField(blank=True, null=True, verbose_name='结束时间')),
            ],
            options={
                'verbose_name': '工作时间段',
                'verbose_name_plural': '工作时间段',
                'db_table': 'cfg_work_period',
            },
        ),
        migrations.CreateModel(
            name='CfgUserInquiry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(blank=True, default=True, null=True, verbose_name='配置开/关')),
                ('value', models.IntegerField(blank=True, null=True, verbose_name='配置值(可选)')),
                ('cfg', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='cfg.CfgBaseInquiry', verbose_name='「查询设置」配置号')),
                ('employee', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='sms.Member', verbose_name='员工号')),
            ],
            options={
                'verbose_name': '「查询设置」用户配置',
                'verbose_name_plural': '「查询设置」用户配置',
                'db_table': 'cfg_user_inquiry',
            },
        ),
    ]
