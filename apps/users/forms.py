from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from apps.users.models import *

__all__ = ['UserLoginForm', 'UserForm', 'UserUpdateForm', 'UserProfileUpdateForm']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        required=False,
        widget=forms.PasswordInput,
        help_text="Tips: 如果密码不修改，请留空.",
    )

    class Meta:
        model = UserProfile
        exclude = ['password', 'last_login']


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['password', 'is_superuser', 'last_login', 'groups']
