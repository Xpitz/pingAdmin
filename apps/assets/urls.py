from django.urls import path

from apps.assets import views

app_name = 'assets'

urlpatterns = [
    path('asset/import/', views.AssetImportView.as_view(), name='asset-import'),
    path('asset/list/', views.AssetListView.as_view(), name='asset-list'),
    path('asset/detail/<int:pk>/', views.AssetDetailView.as_view(), name='asset-detail'),
    path('asset/sync/', views.AssetSyncView.as_view(), name='asset-sync'),
    path('asset/create/', views.AssetCreateView.as_view(), name='asset-create'),
    path('asset/update/<int:pk>/', views.AssetUpdateView.as_view(), name='asset-update'),
    path('asset/delete/', views.AssetDeleteView.as_view(), name='asset-delete'),
    path('asset/export/', views.AssetExportView.as_view(), name='asset-export'),
    path('group/list/', views.AssetGroupListView.as_view(), name='group-list'),
    path('group/create/', views.AssetGroupCreateView.as_view(), name='group-create'),
    path('group/update/<int:pk>/', views.AssetGroupUpdateView.as_view(), name='group-update'),
    path('group/delete/', views.AssetGroupDeleteView.as_view(), name='group-delete'),
]
