from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.conf import settings


class LoggedInPermissionsMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        return super().dispatch(request, *args, **kwargs)
