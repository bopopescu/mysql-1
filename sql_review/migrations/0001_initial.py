# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-27 15:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('statistics', '0003_auto_20170827_2320'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecificationContentForSql',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='0', max_length=255, verbose_name='\u89c4\u8303\u5185\u5bb9')),
            ],
            options={
                'verbose_name': 'SQL\u89c4\u8303\u5185\u5bb9',
                'verbose_name_plural': 'SQL\u89c4\u8303\u5185\u5bb9',
            },
        ),
        migrations.CreateModel(
            name='SpecificationTypeForSql',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='\u516c\u5171\u68c0\u67e5\u9879', max_length=20, verbose_name='\u89c4\u8303\u7c7b\u578b')),
            ],
            options={
                'verbose_name': 'SQL\u89c4\u8303\u7c7b\u578b',
                'verbose_name_plural': 'SQL\u89c4\u8303\u7c7b\u578b',
            },
        ),
        migrations.CreateModel(
            name='SqlBackupRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_record_id', models.IntegerField(default=0, verbose_name='\u5bf9\u5e94\u5ba1\u6838\u8bb0\u5f55\u7684id')),
                ('sequence', models.CharField(default='', max_length=30, verbose_name='\u6267\u884c\u7ed3\u679c\u4e2d\u7684sequence\uff0c\u7528\u6765\u67e5\u627e\u591a\u7528\u7684\u56de\u6eda\u8bed\u53e5')),
                ('backup_db_name', models.CharField(default='', max_length=40, verbose_name='\u5907\u4efd\u6570\u636e\u5e93\u540d')),
                ('sql_sha1', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='\u5982\u679c\u662fosc\uff0c\u4f1a\u6709\u6b64\u503c')),
            ],
        ),
        migrations.CreateModel(
            name='SqlReviewRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_what', models.CharField(max_length=255, verbose_name='\u6267\u884csql\u7684\u76ee\u7684')),
                ('user_name', models.CharField(default='system', max_length=30, verbose_name='\u7533\u8bf7\u4eba')),
                ('pm_name', models.CharField(default='system', max_length=30, verbose_name='\u9879\u76ee\u7ecf\u7406\u540d')),
                ('submit_time', models.DateTimeField(auto_now=True, verbose_name='\u63d0\u4ea4\u8bf7\u6c42\u7684\u65f6\u95f4')),
                ('execute_time', models.DateTimeField(verbose_name='\u8981\u6c42\u6267\u884c\u7684\u65f6\u95f4')),
                ('sql', models.TextField(verbose_name='\u60f3\u8981\u6267\u884c\u7684SQL')),
                ('is_checked', models.IntegerField(default=0, verbose_name='\u673a\u5668\u5ba1\u6838\u72b6\u6001')),
                ('is_submitted', models.IntegerField(default=0, verbose_name='\u63d0\u4ea4\u72b6\u6001')),
                ('is_reviewed', models.IntegerField(default=0, verbose_name='\u9879\u76ee\u7ecf\u7406\u5ba1\u6838\u72b6\u6001')),
                ('is_executed', models.IntegerField(default=0, verbose_name='\u6267\u884c\u72b6\u6001')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statistics.MysqlInstance', verbose_name='\u5bf9\u5e94\u7ec4\u5185\u7684\u5177\u4f53\u5b9e\u4f8b')),
                ('instance_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statistics.MysqlInstanceGroup', verbose_name='\u5b9e\u4f8b\u7ec4')),
            ],
            options={
                'verbose_name': 'SQL\u5ba1\u6838\u63d0\u4ea4\u8bb0\u5f55',
                'verbose_name_plural': 'SQL\u5ba1\u6838\u63d0\u4ea4\u8bb0\u5f55',
            },
        ),
        migrations.AddField(
            model_name='specificationcontentforsql',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sql_review.SpecificationTypeForSql'),
        ),
    ]