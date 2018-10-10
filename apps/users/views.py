# -*- coding: utf-8 -*-
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from utils.generic.shoutcuts import get_object_or_none
from utils.auth.mixins import LoggedInPermissionsMixin
from apps.users.forms import *
from apps.users.models import *


# Create your views here.


class UserListView(LoginRequiredMixin, ListView):
    model = UserProfile
    context_object_name = 'user_obj'
    template_name = 'user/user_list.html'


class UserCreateView(LoggedInPermissionsMixin, CreateView):
    model = UserProfile
    form_class = UserForm
    template_name = 'user/user_create.html'
    context_object_name = 'user_obj'
    success_url = reverse_lazy('users:user-list')
    permission_required = 'users.add_userprofile'
    login_url = 'handler403'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user_role_obj'] = Group.objects.all()
        return context

    def form_valid(self, form):
        user_form = form.save(commit=False)
        user_form.set_password(form.cleaned_data['password'])
        user_form.save()
        return super().form_valid(form)


class UserUpdateView(LoggedInPermissionsMixin, UpdateView):
    model = UserProfile
    form_class = UserUpdateForm
    template_name = 'user/user_update.html'
    context_object_name = 'user_obj'
    success_url = reverse_lazy('users:user-list')
    permission_required = 'users.change_userprofile'
    login_url = 'handler403'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user_role_selected'] = [role.id for role in Group.objects.filter(user=context['user_obj'])]
        context['user_role_obj'] = Group.objects.all()
        return context

    def form_valid(self, form):
        password = form.cleaned_data['password']
        user_form = form.save(commit=False)
        if password:
            user_form.set_password(password)
        user_form.save()
        return super().form_valid(form)


class UserDeleteView(LoggedInPermissionsMixin, DetailView):
    permission_required = 'users.delete_userprofile'
    login_url = 'handler403'

    def get_object(self, *args, **kwargs):
        user_id = self.request.POST.get('user_id')
        return get_object_or_none(UserProfile, id=user_id)

    def post(self, *args, **kwargs):
        user_obj = self.get_object()
        user_obj.delete()
        return HttpResponse(0)


class UserRoleListView(LoginRequiredMixin, ListView):
    model = Group
    context_object_name = 'role_obj'
    template_name = 'role/role_list.html'


class UserRoleCreateView(LoggedInPermissionsMixin, ListView):
    model = Permission
    template_name = 'role/role_create.html'
    context_object_name = 'permission_obj'
    permission_required = 'users.add_userrole'
    login_url = 'handler403'

    def post(self, *args, **kwargs):
        user_role_obj = Group.objects.create(name=self.request.POST.get('role_name'))
        perm_obj = Permission.objects.filter(id__in=self.request.POST.getlist('to[]'))
        user_role_obj.permissions.clear()
        user_role_obj.permissions.add(*perm_obj)
        return HttpResponseRedirect(reverse_lazy('users:role-list'))


class UserRoleUpdateView(LoggedInPermissionsMixin, DetailView):
    model = Group
    template_name = 'role/role_update.html'
    context_object_name = 'role_obj'
    permission_required = 'users.change_userrole'
    login_url = 'handler403'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['permission_obj'] = Permission.objects.all()
        return context

    def post(self, *args, **kwargs):
        user_role_obj = Group.objects.get(name=self.request.POST.get('role_name'))
        user_role_obj.comment = self.request.POST.get('comment')
        user_role_obj.save()
        perm_obj = Permission.objects.filter(id__in=self.request.POST.getlist('to[]'))
        user_role_obj.permissions.clear()
        user_role_obj.permissions.add(*perm_obj)
        return HttpResponseRedirect(reverse_lazy('users:role-list'))


class UserRoleDeleteView(LoggedInPermissionsMixin, DetailView):
    permission_required = 'users.delete_userrole'
    login_url = 'handler403'

    def get_object(self, *args, **kwargs):
        user_role_id = self.request.POST.get('user_role_id')
        return get_object_or_none(Group, id=user_role_id)

    def post(self, *args, **kwargs):
        user_obj = self.get_object()
        user_obj.delete()
        return HttpResponse(0)
