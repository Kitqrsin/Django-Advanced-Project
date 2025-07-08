from django.urls import path

from common import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home-page'),
    path('search_query/', views.search_result, name='search_query')
]