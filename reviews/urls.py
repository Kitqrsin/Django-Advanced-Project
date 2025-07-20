from django.urls import path

from reviews.views import ReviewAddView, DeleteReviewView

urlpatterns = [
    path('add/<int:product_id>/', ReviewAddView.as_view(), name='add-review'),
    path('delete-review/<int:pk>', DeleteReviewView.as_view(), name='delete-review')
]