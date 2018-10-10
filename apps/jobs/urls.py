from django.urls import path

from apps.jobs import views

app_name = 'jobs'

urlpatterns = [
    path('job/cmd/', views.RunCommandView.as_view(), name='run-cmd'),
    path('job/list/', views.JobListView.as_view(), name='job-list'),
    path('job/create/', views.JobCreateView.as_view(), name='job-create'),
    path('job/update/<int:pk>/', views.JobUpdateView.as_view(), name='job-update'),
    path('job/delete/', views.JobDeleteView.as_view(), name='job-delete'),
    path('job/push/', views.JobFilePushView.as_view(), name='job-push'),
    path('type/list/', views.JobTypeListView.as_view(), name='type-list'),
    path('type/create/', views.JobTypeCreateView.as_view(), name='type-create'),
    path('type/update/<int:pk>/', views.JobTypeUpdateView.as_view(), name='type-update'),
    path('type/delete/', views.JobTypeDeleteView.as_view(), name='type-delete'),
]
