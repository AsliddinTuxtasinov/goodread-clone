from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from books.models import Book, BookReview
from books.forms import BookReviewForm


class BooksView(View):
    template_name = "books/books_list.html"

    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get("q", "")
        if search_query:
            books = Book.objects.filter(title__icontains=search_query).order_by('id')

        page_size = request.GET.get("page_size", 2)
        paginator = Paginator(object_list=books, per_page=page_size)

        page_num = request.GET.get("page", 1)
        page_obj = paginator.get_page(number=page_num)

        context = {
            "page_obj": page_obj,
            "search_query": search_query
        }
        return render(request=request, template_name=self.template_name, context=context)


class BookDetailView(View):
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        review_form = BookReviewForm()
        context = {
            "book": book,
            "review_form": review_form
        }
        return render(request=request, template_name="books/book_detail.html", context=context)


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = get_object_or_404(Book, id=id)
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            BookReview.objects.create(user=request.user, book=book, **review_form.cleaned_data)
            return redirect(reverse("books:book_detail", kwargs={"id": book.id}))

        context = {"book": book, "review_form": review_form}
        return render(request=request, template_name="books/book_detail.html", context=context)


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = get_object_or_404(Book, id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review)

        return render(request, "books/review_edit.html", {"book": book, "review": review, "review_form": review_form})

    def post(self, request, book_id, review_id):
        book = get_object_or_404(Book, id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse("books:book_detail", kwargs={"id": book.id}))

        return render(request, "books/review_edit.html", {"book": book, "review": review, "review_form": review_form})


class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = get_object_or_404(Book, id=book_id)
        review = book.bookreview_set.get(id=review_id)
        return render(request, "books/confirm_delete_review.html", {"book": book, "review": review})


class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = get_object_or_404(Book, id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review.delete()
        messages.success(request, "You have successfully deleted this review.")
        return redirect(reverse("books:book_detail", kwargs={"id": book.id}))
