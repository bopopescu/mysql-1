# Generated by Django 2.0.1 on 2018-06-22 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sql_review', '0003_auto_20180510_1850'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cluster_name', models.CharField(max_length=50, verbose_name='集群名称')),
                ('db_name', models.CharField(max_length=30, verbose_name='数据库名称')),
                ('sqllog', models.TextField(verbose_name='执行的sql查询')),
                ('effect_row', models.BigIntegerField(verbose_name='返回行数')),
                ('cost_time', models.CharField(default='', max_length=10, verbose_name='执行耗时')),
                ('username', models.CharField(max_length=30, verbose_name='操作人')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='操作时间')),
                ('sys_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'sql查询日志',
                'verbose_name_plural': 'sql查询日志',
                'db_table': 'query_log',
            },
        ),
    ]