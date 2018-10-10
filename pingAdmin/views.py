from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponse

from djcelery.models import PeriodicTask
from apps.assets.models import *
from apps.jobs.models import *
from apps.users.models import *
from apps.users.forms import *


# Create your views here.

class LoginView(FormView):
    template_name = 'login.html'
    form_class = UserLoginForm
    success_url = '/index/'

    def post(self, *args, **kwargs):
        user_login_form = UserLoginForm(data=self.request.POST)
        if user_login_form.is_valid():
            auth_login(self.request, user_login_form.get_user())
            return redirect(self.success_url)
        return super().get(self.request, *args, **kwargs)


class LogoutView(View):
    def get(self, *args, **kwargs):
        auth_logout(self.request)
        return redirect(reverse_lazy('login'))


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user_obj'] = UserProfile.objects.all()
        context['asset_obj'] = AssetInfo.objects.all()
        context['job_obj'] = JobInfo.objects.all()
        context['task_obj'] = PeriodicTask.objects.all()
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        new_password = self.request.POST.get('new-password')
        confirm_password = self.request.POST.get('confirm-password')
        user_obj = UserProfile.objects.get(username=username)
        print(self.request.POST)
        user_form = UserProfileUpdateForm(self.request.POST, instance=user_obj)

        user = authenticate(username=username, password=password)

        if password and new_password:
            # 密码校验是否正确
            if user:
                if new_password == confirm_password:
                    profile_form = user_form.save(commit=False)
                    profile_form.set_password(new_password)
                    profile_form.save()
                    return HttpResponse(0)
                else:
                    # print(user_form.errors.as_json())
                    print("new password is not same as confirm password.")
                    return HttpResponse(-1)

            else:
                print("password check failed")
                return HttpResponse(-1)

        # 新密码是否输入
        elif password and not new_password:
            print("new password is empty.")
            return HttpResponse(-1)

        else:
            user_form.save()
            return HttpResponse(0)
