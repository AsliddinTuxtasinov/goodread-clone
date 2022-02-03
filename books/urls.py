from django.urls import path
from . import views


app_name = "books"

urlpatterns = [
    path("", views.BooksView.as_view(), name="books_list"),
    path("<int:id>/", views.BookDetailView.as_view(), name="book_detail"),
    path("<int:id>/reviews/", views.AddReviewView.as_view(), name="add_review"),
    path("<int:book_id>/reviews/<int:review_id>/edit/", views.EditReviewView.as_view(), name="edit_review"),
    path("<int:book_id>/reviews/<int:review_id>/delete/confirm/",
         views.ConfirmDeleteReviewView.as_view(), name="confirm_delete_review"),
    path("<int:book_id>/reviews/<int:review_id>/delete/",
         views.DeleteReviewView.as_view(), name="delete_review"),
]
