# -*- coding: utf-8 -*-
import json

from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy

from utils.generic.shoutcuts import get_queryset_or_none
from utils.generic.jobs import generate_job_file
from utils.auth.mixins import LoggedInPermissionsMixin
from utils.remote.salt import SaltApi
from utils.remote.para import ParaApi
from apps.jobs.models import JobInfo, JobType
from apps.assets.models import AssetInfo, AssetGroup
from apps.jobs.forms import *


# Create your views here.

class RunCommandView(LoginRequiredMixin, TemplateView):
    template_name = 'job/run_cmd.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['asset_obj'] = AssetInfo.objects.all()
        context['asset_group_obj'] = AssetGroup.objects.all()
        context['script_obj'] = JobInfo.objects.filter(types__name__iexact='script')
        context['sls_obj'] = JobInfo.objects.filter(types__name__iexact='SLS')
        return context

    def post(self, *args, **kwargs):
        asset = self.request.POST.getlist('assets[]')
        group = self.request.POST.getlist('groups[]')
        module = self.request.POST.get('modules')

        if group:
            asset = [i.hostname for i in AssetInfo.objects.filter(groups__id__in=group)]

        if module == 'cmd.run':
            content = self.request.POST.get('content')
        elif module == 'cmd.script':
            content = self.request.POST.get('scripts')
        else:
            content = self.request.POST.get('sls').split('.')[0]
        result = json.dumps(SaltApi().command_run(asset, module, content))
        return HttpResponse(result)


class JobListView(LoginRequiredMixin, ListView):
    model = JobInfo
    template_name = 'job/job_list.html'
    context_object_name = 'job_obj'


class JobCreateView(LoggedInPermissionsMixin, CreateView):
    model = JobInfo
    form_class = JobForm
    template_name = 'job/job_create.html'
    context_object_name = 'job_obj'
    success_url = reverse_lazy('jobs:job-list')
    permission_required = 'jobs.add_jobinfo'
    login_url = 'handler403'

    def form_valid(self, form):
        generate_job_file(form.cleaned_data)
        return super().form_valid(form)


class JobUpdateView(LoggedInPermissionsMixin, UpdateView):
    model = JobInfo
    form_class = JobForm
    template_name = 'job/job_update.html'
    context_object_name = 'job_obj'
    success_url = reverse_lazy('jobs:job-list')
    permission_required = 'jobs.change_jobinfo'
    login_url = 'handler403'

    def form_valid(self, form):
        generate_job_file(form.cleaned_data)
        return super().form_valid(form)


class JobDeleteView(LoggedInPermissionsMixin, ListView):
    permission_required = 'jobs.delete_jobinfo'
    login_url = 'handler403'

    def get_queryset(self, *args, **kwargs):
        jobs_id = self.request.POST.getlist('jobs_id[]')
        return get_queryset_or_none(JobInfo, id__in=jobs_id)

    def post(self, *args, **kwargs):
        job_queryset = self.get_queryset()
        job_queryset.delete()
        return HttpResponse(0)


class JobFilePushView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        job_id_list = self.request.POST.getlist('jobs_id[]')
        para = ParaApi()
        for i in job_id_list:
            job_name = JobInfo.objects.get(id=i).name
            para.upload(jobname=job_name)

        para.close()
        return HttpResponse(0)


class JobTypeListView(LoginRequiredMixin, ListView):
    model = JobType
    template_name = 'type/type_list.html'
    context_object_name = 'job_type_obj'


class JobTypeCreateView(LoggedInPermissionsMixin, CreateView):
    model = JobType
    form_class = JobTypeForm
    template_name = 'type/type_create.html'
    context_object_name = 'job_type_obj'
    success_url = reverse_lazy('jobs:type-list')
    permission_required = 'jobs.add_jobtype'
    login_url = 'handler403'


class JobTypeUpdateView(LoggedInPermissionsMixin, UpdateView):
    model = JobType
    form_class = JobTypeForm
    template_name = 'type/type_update.html'
    context_object_name = 'job_type_obj'
    success_url = reverse_lazy('jobs:type-list')
    permission_required = 'jobs.change_jobtype'
    login_url = 'handler403'


class JobTypeDeleteView(LoggedInPermissionsMixin, DetailView):
    permission_required = 'jobs.delete_jobtype'
    login_url = 'handler403'

    def get_queryset(self, *args, **kwargs):
        types_id = self.request.POST.getlist('types_id[]')
        return get_queryset_or_none(JobType, id__in=types_id)

    def post(self, *args, **kwargs):
        type_queryset = self.get_queryset()
        type_queryset.delete()
        return HttpResponse(0)
