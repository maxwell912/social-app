from django.urls import path
from . import views

urlpatterns = [
    path('posts/<int:pk>/add/', views.TagCreate.as_view(), name='add'),
    path('posts/<int:pk>/delete/', views.TagDelete.as_view(), name='delete'),
]
