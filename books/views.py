from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from books.models import Book, BookReview
from books.forms import BookReviewForm


# class BooksView(ListView):
#     template_name = "books/books_list.html"
#     queryset = Book.objects.all()
#     context_object_name = "books"
#     paginate_by = 2
#
#     def get_context_data(self, *args, **kwargs):
#         try:
#             context = super().get_context_data()
#         except Http404:
#             self.kwargs['page'] = 1
#             context = super().get_context_data()
#         return context


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

        return render(request=request,
                      template_name=self.template_name,
                      context={
                          "page_obj": page_obj,
                          "search_query": search_query
                      })


# class BookDetailView(DetailView):
#     template_name = "books/book_detail.html"
#     pk_url_kwarg = "id"
#     model = Book
#     context_object_name = 'book'


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
