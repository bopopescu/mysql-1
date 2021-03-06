# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import simplejson

import json
import paramiko

import MySQLdb
from MySQLdb.constants.CLIENT import MULTI_STATEMENTS, MULTI_RESULTS

from .models import MysqlInstanceGroup, MysqlInstance, BackupInstance
#from models import MysqlInstanceGroup, InstanceRelation, MysqlInstance, BackupInstance


from utils.log import my_logger

# Create your views here.


def index(request):
    return render(request, 'base/base.html', {})


def run_meta_sql(sql, db_instance):
    # TODO: 使用原生语句来获取数据库meta信息
    try:
        conn = MySQLdb.connect(host=db_instance.ip, user=db_instance.login_instance_account,
                               passwd=db_instance.login_instance_password, db='mysql', port=db_instance.port,
                               client_flag=MULTI_STATEMENTS | MULTI_RESULTS)
        cur = conn.cursor()
        ret = cur.execute(sql)
        if ret:
            result = cur.fetchall()
        else:
            return 'error'
        cur.close()
        conn.close()
        return result
    except MySQLdb.Error as e:
        print('Mysql Error %d: %s' % (e.args[0], e.args[1]))
        return 'error'


def get_all_information():
    groups = MysqlInstanceGroup.objects.all()
    all_information = list()
    for group in groups:
        information = dict()
        information['nodes'] = MysqlInstance.objects.filter(group=group)
        information['group_name'] = group.name
        all_information.append(information)
    data = {
        'all_information': all_information,
    }
    return data


@login_required()
def instance_list(request):
    data = get_all_information()
    data['sub_module'] = '1_2'
    return render(request, 'statistic/instancelist.html', data)


@login_required()
def instance_pri_list(request):
    data = get_all_information()
    data['sub_module'] = '3_1'
    return render(request, 'statistic/instance_pri_list.html', data)


@login_required()
def processlist(request):
    ip = request.GET.get('ip')
    port = request.GET.get('port', 3306)
    instance = MysqlInstance.objects.get(Q(ip=ip) & Q(port=int(port)))
    sql = 'select * from information_schema.processlist;'
    result = run_meta_sql(sql=sql, db_instance=instance)
    data = {
        'result': result,
        'sub_module': '1_2'
    }
    return render(request, 'statistic/processlist.html', data)


@login_required()
def privileges_list(request):
    ip = request.GET.get('ip')
    port = request.GET.get('port', 3306)
    instance = MysqlInstance.objects.get(Q(ip=ip) & Q(port=int(port)))
    sql = 'SELECT user, host, Select_priv, Insert_priv, Update_priv, Delete_priv FROM mysql.user'
    my_logger(level='info', username=request.user.name, message='读取权限列表，执行SQL: '+sql, path=request.path)
    result = run_meta_sql(sql=sql, db_instance=instance)
    data = {
        'result': result,
        'header': ('user', 'host', 'Select_priv', 'Insert_priv', 'Update_priv', 'Delete_priv'),
        'ip': ip,
        'port': port,
        'sub_module': '3_1'
    }
    return render(request, 'statistic/privileges_list.html', data)


@login_required()
def ajax_get_privileges(request, *args, **kwargs):
    ip = request.POST.get('ip')
    port = request.POST.get('port', 3306)
    host = request.POST.get('host')
    user = request.POST.get('user')
    sql = "show grants for '{}'@'{}'".format(user, host)
    instance = MysqlInstance.objects.get(Q(ip=ip) & Q(port=int(port)))
    result = run_meta_sql(sql=sql, db_instance=instance)
    if result == 'error':
        data = {
            'result': '返回空的结果集或查询错误'
        }
    else:
        str_format_result = ''
        for res in result:
            str_format_result = '{}{}{}'.format(str_format_result, '<br/>', res[0])
        data = {
            'result': str_format_result.lstrip('<br/>').replace('GRANT', '<span style="color: #337ab7;">GRANT</span>')
        }
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False), content_type='application/json')


@login_required()
def topology(request):

    groups = MysqlInstanceGroup.objects.all()
    all_information = list()
    for group in groups:
        information = dict()
        information['nodes'] = MysqlInstance.objects.filter(group=group)
        # information['links'] = InstanceRelation.objects.filter(belong_group=group)
        information['group_name'] = group.name
        all_information.append(information)
    data = {
        'all_information': all_information,
        'sub_module': '1_1'
    }
    return render(request, 'statistic/topology.html', data)


def get_info_by_commend(host, port, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.readlines()
    ssh.close()
    return result

    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect(host, port, username, password)
    # stdin, stdout, stderr = ssh.exec_command(command)
    # ssh.close()
    # print(host, port, username, password, command)
    # return stdout.readlines()


def backup_list(request):
    # 遍历目录查看所有备份文件
    backup_instance = BackupInstance.objects.all()
    all_instance = list()
    for number, instance in enumerate(backup_instance):
        files = list()
        dirs = list()
        dic = {'files': files, 'instance_name': instance.name, 'dirs': dirs}
        mysql_back_dir = get_info_by_commend(instance.ip, instance.port, instance.login_instance_account,
                                             instance.login_instance_password, 'ls /opt/mysql_back')
        for idx, directory in enumerate(mysql_back_dir):
            files_array = get_info_by_commend(instance.ip, instance.port, instance.login_instance_account,
                                             instance.login_instance_password, 'ls /opt/mysql_back/{}'.format(directory))
            dirs.append({
                'pid': 0,
                'id': idx + 1,
                'title': directory.strip()
            })
            for true_file in files_array:
                files.append({
                    'pid': idx + 1,
                    'id': (idx + 1) * 1000 +1,
                    'title': true_file.strip()
                })
        all_instance.append(dic)
    print(all_instance)
    data = {
        'sub_module': '5_1',
        'all_instance': all_instance
    }
    return render(request, 'statistic/backup_list.html', data)
