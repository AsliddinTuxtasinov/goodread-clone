from django.urls import path
from rest_framework import routers
from . import views


app_name = "api"
router = routers.DefaultRouter()

# router.register(prefix=r"reviews/<int:id>/", viewset=views.BookReviewDetailAPIView.as_view(), basename="review_detail")
# router.register(prefix=r"reviews", viewset=views.BookReviewListAPIView.as_view(), basename="reviews_list")


urlpatterns = [
    path("reviews/<int:id>/", views.BookReviewDetailAPIView.as_view(), name="review_detail"),
    path("reviews/", views.BookReviewListAPIView.as_view(), name="reviews_list"),
]

urlpatterns += router.urls
