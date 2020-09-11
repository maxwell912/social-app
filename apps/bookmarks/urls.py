from django.urls import path

from .views import BookmarkCreate, UserBookmarkedPostsView, BookmarkDelete
from .models import BookmarkPost

urlpatterns = [
    path('post/<pk>/bookmark/create', BookmarkCreate.as_view(model=BookmarkPost), name='create-bookmark'),
    path('favorite_post/<pk>', UserBookmarkedPostsView.as_view(), name='favorite'),
    path('post/<pk>/bookmark/delete', BookmarkDelete.as_view(model=BookmarkPost), name='delete-bookmark'),
]
