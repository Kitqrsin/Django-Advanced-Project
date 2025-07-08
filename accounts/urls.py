from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from accounts import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register-user'),
    path('login/', LoginView.as_view(), name='login-user'),
    path('logout/', LogoutView.as_view(), name='logout-user'),
    path('<int:id>/', include([
        path('details/', views.AccountDetailsView.as_view(), name='user-details'),
        path('edit/', views.AccountEditView.as_view(), name='edit-user'),
    ]),
         )

]
