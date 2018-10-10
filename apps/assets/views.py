# -*- coding: utf-8 -*-
import csv
import codecs
import chardet
from io import StringIO

from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q

from utils.generic.shoutcuts import get_object_or_none, get_queryset_or_none
from utils.auth.mixins import LoggedInPermissionsMixin
from apps.assets.models import AssetInfo, AssetGroup
from apps.assets.forms import *
from apps.tasks.tasks import *


# Create your views here.


class AssetListView(LoginRequiredMixin, ListView):
    model = AssetInfo
    template_name = 'asset/asset_list.html'
    context_object_name = 'asset_obj'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data()
        context['asset_group_obj'] = AssetGroup.objects.all()
        return context


class AssetDetailView(LoginRequiredMixin, DetailView):
    model = AssetInfo
    template_name = 'asset/asset_detail.html'
    context_object_name = 'asset_obj'


class AssetSyncView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        asset_id_list = self.request.POST.getlist('assets_id[]')
        if asset_id_list:
            asset_name_list = [AssetInfo.objects.get(id=i).hostname for i in asset_id_list]
        else:
            asset_name_list = [i.hostname for i in AssetInfo.objects.all()]

        # 调用tasks同步信息
        # sync_info.delay(asset_name_list)
        # 遍历方式获取信息，堵塞方式
        sync_info(asset_name_list)
        return HttpResponse(0)


class AssetCreateView(LoggedInPermissionsMixin, CreateView):
    model = AssetInfo
    form_class = AssetForm
    template_name = 'asset/asset_create.html'
    context_object_name = 'asset_obj'
    success_url = reverse_lazy('assets:asset-list')
    permission_required = 'assets.add_assetinfo'
    login_url = 'handler403'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['asset_group_obj'] = AssetGroup.objects.all()
        return context


class AssetUpdateView(LoggedInPermissionsMixin, UpdateView):
    model = AssetInfo
    form_class = AssetForm
    template_name = 'asset/asset_update.html'
    context_object_name = 'asset_obj'
    success_url = reverse_lazy('assets:asset-list')
    permission_required = 'assets.change_assetinfo'
    login_url = 'handler403'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['asset_group_obj'] = AssetGroup.objects.all()
        return context


class AssetDeleteView(LoginRequiredMixin, DetailView):
    def get_queryset(self, *args, **kwargs):
        assets_id = self.request.POST.getlist('assets_id[]')
        return get_queryset_or_none(AssetInfo, id__in=assets_id)

    def post(self, *args, **kwargs):
        asset_queryset = self.get_queryset()
        asset_queryset.delete()
        return HttpResponse(0)


class AssetExportView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        # 定义导出csv字段
        fields = [
            field for field in AssetInfo._meta.fields
            # 选择已勾选的字段
            if field.name in list(self.request.GET.dict().keys())
        ]
        export_scope = self.request.GET.get('exportScope')
        group_id_list = self.request.GET.getlist('groupIdList')
        asset_id = self.request.GET.get('assetId')
        asset_id_list = [] if not asset_id else asset_id.split(',')

        # 定义导出文件名及导出资产
        filename = 'asset.csv'

        if export_scope == 'part' and asset_id_list:
            assets = AssetInfo.objects.filter(Q(groups_id__in=group_id_list) & Q(id__in=asset_id_list))
        else:
            assets = AssetInfo.objects.filter(groups_id__in=group_id_list)

        # 声明一个csv的响应
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename

        # csv的响应的编码格式声明
        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response, dialect='excel', quoting=csv.QUOTE_MINIMAL)

        # 定义标题字段并写入内容
        header = [field.verbose_name for field in fields]
        writer.writerow(header)

        # 循环写入资产信息
        for asset in assets:
            data = [getattr(asset, field.name) for field in fields]
            writer.writerow(data)
        return response


class AssetImportView(LoginRequiredMixin, FormView):
    form_class = FileForm

    def post(self, *args, **kwargs):
        form = FileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            # 检测上传文件编码
            det_result = chardet.detect(f.read())
            # reset file seek index
            f.seek(0)
            file_data = f.read().decode(det_result['encoding']).strip(codecs.BOM_UTF8.decode())
            csv_file = StringIO(file_data)
            reader = csv.reader(csv_file)
            # 以列表形式记录csv文件中的每条记录
            csv_data = [row for row in reader]
            fields = [
                field for field in AssetInfo._meta.fields
            ]
            header = csv_data[0]
            mapping_reverse = {field.verbose_name: field.name for field in fields}
            # 以verbose_name匹配上传文件的header信息
            attr = [mapping_reverse.get(n, None) for n in header]
            created, updated, failed = [], [], []
            assets = []
            for row in csv_data[1:]:
                # 跳过记录之间的空行
                if set(row) == {''}:
                    continue

                asset_dict = dict(zip(attr, row))
                for k, v in asset_dict.items():
                    v = v.strip()
                    if k == 'groups':
                        v = get_object_or_none(AssetGroup, name=v)
                    asset_dict[k] = v

                asset_id = asset_dict.pop('id', None)
                asset = get_object_or_none(AssetInfo, id=asset_id) if asset_id else None
                # 资产添加
                if not asset:
                    try:
                        if len(AssetInfo.objects.filter(hostname=asset_dict.get('hostname'))):
                            raise Exception('already exists')
                        # 遇到错误执行回滚操作
                        with transaction.atomic():
                            asset = AssetInfo.objects.create(**asset_dict)
                            created.append(asset_dict['hostname'])
                            assets.append(asset)
                    except Exception as e:
                        failed.append('%s: %s' % (asset_dict['hostname'], str(e)))
                # 资产更新
                else:
                    for k, v in asset_dict.items():
                        if v:
                            setattr(asset, k, v)
                    try:
                        asset.save()
                        updated.append(asset_dict['hostname'])
                    except Exception as e:
                        failed.append('%s: %s' % (asset_dict['hostname'], str(e)))
            print(created, updated, failed)
        else:
            print(form.errors.as_json)

        return HttpResponseRedirect(reverse_lazy('assets:asset-list'))


class AssetGroupListView(LoginRequiredMixin, ListView):
    model = AssetGroup
    template_name = 'group/group_list.html'
    context_object_name = 'asset_group_obj'


class AssetGroupCreateView(LoggedInPermissionsMixin, CreateView):
    model = AssetGroup
    form_class = AssetGroupForm
    template_name = 'group/group_create.html'
    context_object_name = 'asset_group_obj'
    success_url = reverse_lazy('assets:group-list')
    permission_required = 'assets.add_assetgroup'
    login_url = 'handler403'


class AssetGroupUpdateView(LoggedInPermissionsMixin, UpdateView):
    model = AssetGroup
    form_class = AssetGroupForm
    template_name = 'group/group_update.html'
    context_object_name = 'asset_group_obj'
    success_url = reverse_lazy('assets:group-list')
    permission_required = 'assets.change_assetgroup'
    login_url = 'handler403'


class AssetGroupDeleteView(LoggedInPermissionsMixin, DetailView):
    permission_required = 'assets.delete_assetgroup'
    login_url = 'handler403'

    def get_queryset(self, *args, **kwargs):
        groups_id = self.request.POST.getlist('groups_id[]')
        return get_queryset_or_none(AssetGroup, id__in=groups_id)

    def post(self, *args, **kwargs):
        group_queryset = self.get_queryset()
        group_queryset.delete()
        return HttpResponse(0)
