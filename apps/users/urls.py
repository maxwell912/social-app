from django.urls import path

from apps.users.views import UserProfileUpdateView, UserProfileView

urlpatterns = [
    path('edit/<int:pk>/', UserProfileUpdateView.as_view(), name='edit'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),

]
