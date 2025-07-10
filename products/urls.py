from django.urls import path

from products import views

urlpatterns = [
    path('<int:id>/', views.ProductDetailsView.as_view(), name='product-details')
]