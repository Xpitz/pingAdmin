"""pingAdmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403

from rest_framework import routers

from .views import LoginView, LogoutView, IndexView, ProfileView
from apps.assets import api as assets_api
from apps.users import api as users_api

router = routers.DefaultRouter()
router.register(r'userProfile', users_api.UserProfileViewSet)
router.register(r'assetInfo', assets_api.AssetViewSet)
router.register(r'assetGroup', assets_api.AssetGroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('index/', IndexView.as_view(), name='index'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('assets/', include('apps.assets.urls', namespace='assets')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('tasks/', include('apps.tasks.urls', namespace='tasks')),
    path('jobs/', include('apps.jobs.urls', namespace='jobs')),

    path('403/', handler403, kwargs={'exception': Exception('Permission Denied')}, name='handler403'),

    path('api/v1/', include(router.urls)),


]
