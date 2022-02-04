from django.urls import path
from . import views


app_name = "api"

urlpatterns = [
    path("<int:id>/reviews/", views.BookReviewDetailAPIView.as_view(), name="review_detail"),
    path("reviews/", views.BookReviewListAPIView.as_view(), name="reviews_list"),
]
