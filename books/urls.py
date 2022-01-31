from django.urls import path
from . import views


app_name = "books"

urlpatterns = [
    path("", views.BooksView.as_view(), name="books_list"),
    path("<int:id>", views.BookDetailView.as_view(), name="book_detail"),
    path("<int:id>/reviews/", views.AddReviewView.as_view(), name="add_review"),
]
