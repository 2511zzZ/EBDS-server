# Generated by Django 2.2.7 on 2019-11-16 16:03

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
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('sex', models.CharField(blank=True, max_length=255, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('birthplace', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.IntegerField(blank=True, choices=[(0, '工人'), (1, '大组长'), (2, '经理'), (3, '总经理')], null=True)),
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
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': '小组结构',
                'verbose_name_plural': '小组结构',
                'db_table': 'sms_team',
            },
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('employee', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='employee_workshop', to='sms.Member')),
            ],
            options={
                'verbose_name': '车间结构',
                'verbose_name_plural': '车间结构',
                'db_table': 'sms_workshop',
            },
        ),
        migrations.CreateModel(
            name='TeamStatMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stat_id', models.IntegerField()),
                ('morning_shift_id', models.IntegerField(blank=True, null=True)),
                ('middle_shift_id', models.IntegerField(blank=True, null=True)),
                ('night_shift_id', models.IntegerField(blank=True, null=True)),
                ('update_time', models.DateField(blank=True, null=True)),
                ('team', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='team_stat_member', to='sms.Team')),
            ],
            options={
                'verbose_name': '小组工人排班',
                'verbose_name_plural': '小组工人排班',
                'db_table': 'sms_team_stat_member',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('employee', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='employee_group', to='sms.Member')),
            ],
            options={
                'verbose_name': '大组结构',
                'verbose_name_plural': '大组结构',
                'db_table': 'sms_group',
            },
        ),
        migrations.CreateModel(
            name='TeamGroupWorkshop',
            fields=[
                ('team', models.OneToOneField(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='level_relate', serialize=False, to='sms.Team')),
                ('group', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='level_relate', to='sms.Group')),
                ('workshop', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='level_relate', to='sms.Workshop')),
            ],
            options={
                'verbose_name': '小组-大组-车间层级关系',
                'verbose_name_plural': '小组-大组-车间层级关系',
                'db_table': 'sms_team_group_workshop',
            },
        ),
    ]
