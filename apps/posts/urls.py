import os

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    PostCreate,
    PostListView,
    PostDetailView,
    CommentCreate,
    PostUpdate,
    AttachmentsZipView,
    create_task,
    PostDeleteView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<substring>/<attr>/', PostListView.as_view(), name='posts-filter'),

    path('create/', PostCreate.as_view(), name='post-create'),
    path('update/<int:pk>', PostUpdate.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path(
        'post/<int:pk>/add_comment/',
        CommentCreate.as_view(),
        name='add-comment'
    ),

    path('zip/create/<int:pk>', create_task, name='attachments-task'),
    path(
        'attachments/<task_id>',
        AttachmentsZipView.as_view(),
        name='attachments-result'
    ),

]

urlpatterns += static(
    '/attachments/', document_root=os.path.join(settings.MEDIA_ROOT, 'attachments')
)
