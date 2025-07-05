from django.contrib.auth.views import LoginView
from django.urls import path

from accounts import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register-user'),
    path('login/', LoginView.as_view(), name='login-user')
]