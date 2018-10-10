from django.urls import path

from apps.tasks import views

app_name = 'tasks'

urlpatterns = [
    path('crontab/list/', views.CrontabListView.as_view(), name='crontab-list'),
    path('crontab/create/', views.CrontabCreateView.as_view(), name='crontab-create'),
    path('crontab/update/<int:pk>/', views.CrontabUpdateView.as_view(), name='crontab-update'),
    path('crontab/delete/', views.CrontabDeleteView.as_view(), name='crontab-delete'),
    path('interval/list/', views.IntervalListView.as_view(), name='interval-list'),
    path('interval/create/', views.IntervalCreateView.as_view(), name='interval-create'),
    path('interval/update/<int:pk>/', views.IntervalUpdateView.as_view(), name='interval-update'),
    path('interval/delete/', views.IntervalDeleteView.as_view(), name='interval-delete'),
    path('task/list/', views.PeriodicTaskListView.as_view(), name='task-list'),
    path('task/create/', views.PeriodicTaskCreateView.as_view(), name='task-create'),
    path('task/update/<int:pk>/', views.PeriodicTaskUpdateView.as_view(), name='task-update'),
    path('task/delete/', views.PeriodicTaskDeleteView.as_view(), name='task-delete'),
    path('task/result/list/', views.TaskResultListView.as_view(), name='task-result-list'),
]
