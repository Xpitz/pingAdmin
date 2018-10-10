# -*- coding: utf-8 -*-
from celery import shared_task
from utils.remote.salt import *
from apps.assets.models import AssetInfo

salt = SaltApi()

__all__ = ['sync_info', 'cmd_run']


@shared_task
def sync_info(asset_name_list):
    result = {}
    salt_key = salt.list_all_key()[0]
    system_info = salt.grains_items(asset_name_list)
    for i in asset_name_list:
        asset_obj = AssetInfo.objects.filter(hostname=i)
        if i in salt_key:
            asset_obj.update(os=system_info[i].get('os'),
                             os_release=system_info[i].get('osrelease'),
                             cpu_model=system_info[i].get('cpu_model'),
                             cpu_count=system_info[i].get('num_cpus'),
                             mem_total=system_info[i].get('mem_total'),
                             sn=system_info[i].get('serialnumber'))
            result[i] = True
        else:
            result[i] = False

    return result


@shared_task
def cmd_run(asset_name_list, command):
    result = salt.cmd_run(tgt=asset_name_list, arg=command)
    return result
