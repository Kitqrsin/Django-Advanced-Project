from django.urls import path

from cart import views

urlpatterns = [
    path('', views.CartDetailsView.as_view(), name='cart')
]