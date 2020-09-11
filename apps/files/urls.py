from django.urls import path

from apps.files.views import FileDetail, FileDelete

urlpatterns = [
    path('<int:pk>/', FileDetail.as_view(), name='get-file'),
    path('<int:pk>/delete/', FileDelete.as_view(), name='delete-file'),
]
