from django.urls import path

from cart import views
from cart.views import add_to_cart

urlpatterns = [
    path('', views.CartDetailsView.as_view(), name='cart'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('subtract-from-cart/', views.subtract_from_cart, name='subtract-from-cart'),
]