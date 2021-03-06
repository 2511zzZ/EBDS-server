# Generated by Django 2.1.11 on 2019-12-03 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StandardBasicAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_id', models.IntegerField(blank=True, null=True)),
                ('time', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'standard_basic_action',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StandardDpt',
            fields=[
                ('s_efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='标准效率')),
                ('s_accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='标准准确率')),
                ('s_workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='标准有效工时')),
                ('dpt', models.OneToOneField(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='sms.Dpt', verbose_name='生产部号')),
            ],
            options={
                'verbose_name': '生产部标准指标',
                'verbose_name_plural': '生产部标准指标',
                'db_table': 'standard_dpt',
            },
        ),
        migrations.CreateModel(
            name='StandardGroup',
            fields=[
                ('s_efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='标准效率')),
                ('s_accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='标准准确率')),
                ('s_workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='标准有效工时')),
                ('group', models.OneToOneField(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='group_standard', serialize=False, to='sms.Group', verbose_name='大组号')),
            ],
            options={
                'verbose_name': '大组标准指标',
                'verbose_name_plural': '大组标准指标',
                'db_table': 'standard_group',
            },
        ),
        migrations.CreateModel(
            name='StandardTeam',
            fields=[
                ('s_efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='标准效率')),
                ('s_accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='标准准确率')),
                ('s_workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='标准有效工时')),
                ('team', models.OneToOneField(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='team_standard', serialize=False, to='sms.Team', verbose_name='小组号')),
            ],
            options={
                'verbose_name': '小组标准指标',
                'verbose_name_plural': '小组标准指标',
                'db_table': 'standard_team',
            },
        ),
        migrations.CreateModel(
            name='StandardWorkshop',
            fields=[
                ('s_efficiency', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='标准效率')),
                ('s_accuracy', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='标准准确率')),
                ('s_workhour', models.DecimalField(blank=True, decimal_places=1, max_digits=6, null=True, verbose_name='标准有效工时')),
                ('workshop', models.OneToOneField(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='workshop_standard', serialize=False, to='sms.Workshop', verbose_name='车间号')),
            ],
            options={
                'verbose_name': '车间标准指标',
                'verbose_name_plural': '车间标准指标',
                'db_table': 'standard_workshop',
            },
        ),
    ]
