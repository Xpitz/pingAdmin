# -*- coding: utf-8 -*-
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy

from celery.app.control import Inspect
from celery import current_app

from utils.generic.shoutcuts import get_object_or_none, get_queryset_or_none
from utils.auth.mixins import LoggedInPermissionsMixin
from djcelery.models import TaskMeta, CrontabSchedule, IntervalSchedule, PeriodicTask
from apps.tasks.forms import *


# Create your views here.


class CrontabListView(LoginRequiredMixin, ListView):
    model = CrontabSchedule
    template_name = 'crontab/crontab_list.html'
    context_object_name = 'crontab_obj'


class CrontabCreateView(LoggedInPermissionsMixin, CreateView):
    model = CrontabSchedule
    form_class = CrontabScheduleForm
    template_name = 'crontab/crontab_create.html'
    context_object_name = 'crontab_obj'
    success_url = reverse_lazy('tasks:crontab-list')
    permission_required = 'djcelery.add_crontabschedule'
    login_url = 'handler403'


class CrontabUpdateView(LoggedInPermissionsMixin, UpdateView):
    model = CrontabSchedule
    form_class = CrontabScheduleForm
    template_name = 'crontab/crontab_update.html'
    context_object_name = 'crontab_obj'
    success_url = reverse_lazy('tasks:crontab-list')
    permission_required = 'djcelery.change_crontabschedule'
    login_url = 'handler403'


class CrontabDeleteView(LoggedInPermissionsMixin, DetailView):
    permission_required = 'djcelery.delete_crontabschedule'
    login_url = 'handler403'

    def get_queryset(self, *args, **kwargs):
        crons_id = self.request.POST.getlist('crons_id[]')
        return get_queryset_or_none(CrontabSchedule, id__in=crons_id)

    def post(self, *args, **kwargs):
        cron_queryset = self.get_queryset()
        cron_queryset.delete()
        return HttpResponse(0)


class IntervalListView(LoginRequiredMixin, ListView):
    model = IntervalSchedule
    template_name = 'interval/interval_list.html'
    context_object_name = 'interval_obj'


class IntervalCreateView(LoggedInPermissionsMixin, CreateView):
    model = IntervalSchedule
    form_class = IntervalScheduleForm
    template_name = 'interval/interval_create.html'
    context_object_name = 'interval_obj'
    success_url = reverse_lazy('tasks:interval-list')
    permission_required = 'djcelery.add_intervalschedule'
    login_url = 'handler403'


class IntervalUpdateView(LoggedInPermissionsMixin, UpdateView):
    model = IntervalSchedule
    form_class = IntervalScheduleForm
    template_name = 'interval/interval_update.html'
    context_object_name = 'interval_obj'
    success_url = reverse_lazy('tasks:interval-list')
    permission_required = 'djcelery.change_intervalschedule'
    login_url = 'handler403'


class IntervalDeleteView(LoggedInPermissionsMixin, DetailView):
    permission_required = 'djcelery.delete_intervalschedule'
    login_url = 'handler403'

    def get_queryset(self, *args, **kwargs):
        interval_id = self.request.POST.getlist('intervals_id[]')
        return get_queryset_or_none(IntervalSchedule, id__in=interval_id)

    def post(self, *args, **kwargs):
        interval_queryset = self.get_queryset()
        interval_queryset.delete()
        return HttpResponse(0)


class PeriodicTaskListView(LoginRequiredMixin, ListView):
    model = PeriodicTask
    template_name = 'task/task_list.html'
    context_object_name = 'task_obj'


class PeriodicTaskCreateView(LoggedInPermissionsMixin, CreateView):
    model = PeriodicTask
    form_class = PeriodicTaskForm
    template_name = 'task/task_create.html'
    context_object_name = 'task_obj'
    success_url = reverse_lazy('tasks:task-list')
    permission_required = 'djcelery.add_periodictask'
    login_url = 'handler403'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data()
        # 需要启动celery，如果不启动，则返回空列表
        try:
            context['registered_tasks'] = list(Inspect(app=current_app).registered().values())[0]
        except Exception as e:
            context['registered_tasks'] = []

        return context


class PeriodicTaskUpdateView(LoggedInPermissionsMixin, UpdateView):
    model = PeriodicTask
    form_class = PeriodicTaskForm
    template_name = 'task/task_update.html'
    context_object_name = 'task_obj'
    success_url = reverse_lazy('tasks:task-list')
    permission_required = 'djcelery.change_periodictask'
    login_url = 'handler403'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data()
        # 需要启动celery，如果不启动，则返回空列表
        try:
            context['registered_tasks'] = list(Inspect(app=current_app).registered().values())[0]
        except Exception as e:
            context['registered_tasks'] = []

        return context


class PeriodicTaskDeleteView(LoggedInPermissionsMixin, DetailView):
    permission_required = 'djcelery.delete_periodictask'
    login_url = 'handler403'

    def get_object(self, *args, **kwargs):
        task_id = self.request.POST.get('task_id')
        return get_object_or_none(PeriodicTask, id=task_id)

    def post(self, *args, **kwargs):
        task_obj = self.get_object()
        task_obj.delete()
        return HttpResponse(0)


class TaskResultListView(LoginRequiredMixin, ListView):
    model = TaskMeta
    template_name = 'task/task_result_list.html'
    context_object_name = 'task_obj'
