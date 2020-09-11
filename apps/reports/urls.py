import os

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report-list'),
    path('posts/<int:pk>/', views.ReportCreate.as_view(), name='report-create'),

    path('list/create/', views.ReportListTask.as_view(), name='create-list-task'),
    path('list/result/<task_id>', views.ReportListResultView.as_view(), name='report-result'),
]

urlpatterns += static(
    '/reports/', document_root=os.path.join(settings.MEDIA_ROOT, 'reports')
)
