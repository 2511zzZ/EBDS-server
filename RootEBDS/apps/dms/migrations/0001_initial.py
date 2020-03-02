# Generated by Django 2.1.11 on 2019-12-03 19:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DmsActionInfo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('action_id', models.IntegerField()),
                ('stat_id', models.IntegerField(blank=True, null=True)),
                ('spend_sec', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'dms_action_info',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DmsDptAvg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='平均工作效率')),
                ('a_accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='平均准确率')),
                ('a_workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='平均有效工时')),
                ('time', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='时间')),
                ('dpt_id', models.IntegerField(verbose_name='生产部号')),
            ],
            options={
                'verbose_name': '生产部实时平均工作数据(最近)',
                'verbose_name_plural': '生产部实时平均工作数据(最近)',
                'db_table': 'dms_dpt_avg',
            },
        ),
        migrations.CreateModel(
            name='DmsDptDaily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日效率')),
                ('accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日准确率')),
                ('workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日有效工时')),
                ('time', models.DateField(blank=True, db_index=True, default=datetime.date.today, null=True, verbose_name='日期')),
                ('dpt_id', models.IntegerField(db_index=True, verbose_name='生产部号')),
            ],
            options={
                'verbose_name': '生产部历史工作记录(每日)',
                'verbose_name_plural': '生产部历史工作记录(每日)',
                'db_table': 'dms_dpt_daily',
            },
        ),
        migrations.CreateModel(
            name='DmsDptOnline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='实时效率')),
                ('accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='实时准确率')),
                ('workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='实时有效工时')),
                ('time', models.DateTimeField(blank=True, db_index=True, default=datetime.datetime.now, null=True, verbose_name='时间')),
                ('dpt_id', models.IntegerField(db_index=True, verbose_name='生产部号')),
            ],
            options={
                'verbose_name': '生产部实时工作数据(24小时内)',
                'verbose_name_plural': '生产部实时工作数据(24小时内)',
                'db_table': 'dms_dpt_online',
            },
        ),
        migrations.CreateModel(
            name='DmsGroupAvg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='平均工作效率')),
                ('a_accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='平均准确率')),
                ('a_workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='平均有效工时')),
                ('time', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='时间')),
                ('group_id', models.IntegerField(verbose_name='大组号')),
            ],
            options={
                'verbose_name': '大组实时平均工作数据(最近)',
                'verbose_name_plural': '大组实时平均工作数据(最近)',
                'db_table': 'dms_group_avg',
            },
        ),
        migrations.CreateModel(
            name='DmsGroupDaily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日效率')),
                ('accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日准确率')),
                ('workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日有效工时')),
                ('time', models.DateField(blank=True, db_index=True, default=datetime.date.today, null=True, verbose_name='日期')),
                ('group_id', models.IntegerField(db_index=True, verbose_name='大组号')),
            ],
            options={
                'verbose_name': '大组历史工作记录(每日)',
                'verbose_name_plural': '大组历史工作记录(每日)',
                'db_table': 'dms_group_daily',
            },
        ),
        migrations.CreateModel(
            name='DmsGroupOnline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='实时效率')),
                ('accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='实时准确率')),
                ('workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='实时有效工时')),
                ('time', models.DateTimeField(blank=True, db_index=True, default=datetime.datetime.now, null=True, verbose_name='时间')),
                ('group_id', models.IntegerField(db_index=True, verbose_name='大组号')),
            ],
            options={
                'verbose_name': '大组实时工作数据(24小时内)',
                'verbose_name_plural': '大组实时工作数据(24小时内)',
                'db_table': 'dms_group_online',
            },
        ),
        migrations.CreateModel(
            name='DmsStatAvg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='平均工作效率')),
                ('a_accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='平均准确率')),
                ('a_workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='平均有效工时')),
                ('time', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='时间')),
                ('stat_id', models.IntegerField(db_index=True, verbose_name='工位号')),
            ],
            options={
                'verbose_name': '工位实时平均工作数据(最近)',
                'verbose_name_plural': '工位实时平均工作数据(最近)',
                'db_table': 'dms_stat_avg',
            },
        ),
        migrations.CreateModel(
            name='DmsStatDaily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日效率')),
                ('accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日准确率')),
                ('workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日有效工时')),
                ('time', models.DateField(blank=True, db_index=True, default=datetime.date.today, null=True, verbose_name='日期')),
                ('stat_id', models.IntegerField(db_index=True, verbose_name='工位号')),
            ],
            options={
                'verbose_name': '工位历史工作记录(每日)',
                'verbose_name_plural': '工位历史工作记录(每日)',
                'db_table': 'dms_stat_daily',
            },
        ),
        migrations.CreateModel(
            name='DmsStatOnline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='实时效率')),
                ('accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='实时准确率')),
                ('workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='实时有效工时')),
                ('time', models.DateTimeField(blank=True, db_index=True, default=datetime.datetime.now, null=True, verbose_name='时间')),
                ('stat_id', models.IntegerField(db_index=True, verbose_name='工位号')),
            ],
            options={
                'verbose_name': '工位实时工作数据(24小时内)',
                'verbose_name_plural': '工位实时工作数据(24小时内)',
                'db_table': 'dms_stat_online',
            },
        ),
        migrations.CreateModel(
            name='DmsTeamAvg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='平均工作效率')),
                ('a_accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='平均准确率')),
                ('a_workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='平均有效工时')),
                ('time', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='时间')),
                ('team_id', models.IntegerField(db_index=True, verbose_name='小组号')),
            ],
            options={
                'verbose_name': '小组实时平均工作数据(最近)',
                'verbose_name_plural': '小组实时平均工作数据(最近)',
                'db_table': 'dms_team_avg',
            },
        ),
        migrations.CreateModel(
            name='DmsTeamDaily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日效率')),
                ('accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日准确率')),
                ('workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日有效工时')),
                ('time', models.DateField(blank=True, db_index=True, default=datetime.date.today, null=True, verbose_name='日期')),
                ('team_id', models.IntegerField(db_index=True, verbose_name='小组号')),
            ],
            options={
                'verbose_name': '小组历史工作记录(每日)',
                'verbose_name_plural': '小组历史工作记录(每日)',
                'db_table': 'dms_team_daily',
            },
        ),
        migrations.CreateModel(
            name='DmsTeamOnline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='实时效率')),
                ('accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='实时准确率')),
                ('workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='实时有效工时')),
                ('time', models.DateTimeField(blank=True, db_index=True, default=datetime.datetime.now, null=True, verbose_name='时间')),
                ('team_id', models.IntegerField(db_index=True, verbose_name='小组号')),
            ],
            options={
                'verbose_name': '小组实时工作数据(24小时内)',
                'verbose_name_plural': '小组实时工作数据(24小时内)',
                'db_table': 'dms_team_online',
            },
        ),
        migrations.CreateModel(
            name='DmsWorkerDaily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日效率')),
                ('accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日准确率')),
                ('workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日有效工时')),
                ('time', models.DateField(blank=True, db_index=True, default=datetime.date.today, null=True, verbose_name='日期')),
                ('worker_id', models.IntegerField(db_index=True, verbose_name='员工号')),
            ],
            options={
                'verbose_name': '工人历史工作记录(每日)',
                'verbose_name_plural': '工人历史工作记录(每日)',
                'db_table': 'dms_worker_daily',
            },
        ),
        migrations.CreateModel(
            name='DmsWorkshopAvg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='平均工作效率')),
                ('a_accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='平均准确率')),
                ('a_workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='平均有效工时')),
                ('time', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='时间')),
                ('workshop_id', models.IntegerField(verbose_name='车间号')),
            ],
            options={
                'verbose_name': '车间实时平均工作数据(最近)',
                'verbose_name_plural': '车间实时平均工作数据(最近)',
                'db_table': 'dms_workshop_avg',
            },
        ),
        migrations.CreateModel(
            name='DmsWorkshopDaily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日效率')),
                ('accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日准确率')),
                ('workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='每日有效工时')),
                ('time', models.DateField(blank=True, db_index=True, default=datetime.date.today, null=True, verbose_name='日期')),
                ('workshop_id', models.IntegerField(db_index=True, verbose_name='车间号')),
            ],
            options={
                'verbose_name': '车间历史工作记录(每日)',
                'verbose_name_plural': '车间历史工作记录(每日)',
                'db_table': 'dms_workshop_daily',
            },
        ),
        migrations.CreateModel(
            name='DmsWorkshopOnline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='实时效率')),
                ('accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='实时准确率')),
                ('workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='实时有效工时')),
                ('time', models.DateTimeField(blank=True, db_index=True, default=datetime.datetime.now, null=True, verbose_name='时间')),
                ('workshop_id', models.IntegerField(db_index=True, verbose_name='车间号')),
            ],
            options={
                'verbose_name': '车间实时工作数据(24小时内)',
                'verbose_name_plural': '车间实时工作数据(24小时内)',
                'db_table': 'dms_workshop_online',
            },
        ),
        migrations.AlterIndexTogether(
            name='dmsworkshoponline',
            index_together={('workshop_id', 'time')},
        ),
        migrations.AlterIndexTogether(
            name='dmsworkshopdaily',
            index_together={('workshop_id', 'time')},
        ),
        migrations.AlterIndexTogether(
            name='dmsworkerdaily',
            index_together={('worker_id', 'time')},
        ),
        migrations.AlterIndexTogether(
            name='dmsteamonline',
            index_together={('team_id', 'time')},
        ),
        migrations.AlterIndexTogether(
            name='dmsteamdaily',
            index_together={('team_id', 'time')},
        ),
        migrations.AlterIndexTogether(
            name='dmsstatonline',
            index_together={('stat_id', 'time')},
        ),
        migrations.AlterIndexTogether(
            name='dmsstatdaily',
            index_together={('stat_id', 'time')},
        ),
        migrations.AlterIndexTogether(
            name='dmsgrouponline',
            index_together={('group_id', 'time')},
        ),
        migrations.AlterIndexTogether(
            name='dmsgroupdaily',
            index_together={('group_id', 'time')},
        ),
    ]
