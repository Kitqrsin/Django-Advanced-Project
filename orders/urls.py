from django.urls import path

from orders import views

urlpatterns = [
    path('', views.CheckoutView.as_view(), name='checkout'),
    path("api/econt-offices/", views.econt_offices_api, name="econt_offices_api"),

]
