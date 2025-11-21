from django.urls import path
from .views import UserProfileAPI,UserProfileAPIView

urlpatterns = [
    path('users/',UserProfileAPI.as_view()),
    path('users/<int:pk>/',UserProfileAPIView.as_view())
]