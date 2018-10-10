from django.urls import path
from apps.users import views

app_name = 'users'

urlpatterns = [
    path('user/list/', views.UserListView.as_view(), name='user-list'),
    path('user/create/', views.UserCreateView.as_view(), name='user-create'),
    path('user/update/<int:pk>/', views.UserUpdateView.as_view(), name='user-update'),
    path('user/delete/', views.UserDeleteView.as_view(), name='user-delete'),
    path('role/list/', views.UserRoleListView.as_view(), name='role-list'),
    path('role/create/', views.UserRoleCreateView.as_view(), name='role-create'),
    path('role/update/<int:pk>/', views.UserRoleUpdateView.as_view(), name='role-update'),
    path('role/delete/', views.UserRoleDeleteView.as_view(), name='role-delete'),
]
