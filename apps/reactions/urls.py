from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/create/', views.ReactionCreate.as_view(), name='create'),
    path('<int:pk>/delete/', views.ReactionDelete.as_view(), name='delete'),
]
