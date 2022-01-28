from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from books.models import Book


class BooksView(ListView):
    template_name = "books/books_list.html"
    queryset = Book.objects.all()
    context_object_name = "books"


# class BooksView(View):
#     template_name = "books/books_list.html"
#
#     def get(self, request):
#         books = Book.objects.all()
#         return render(request=request, template_name=self.template_name, context={"books": books})


class BookDetailView(DetailView):
    template_name = "books/book_detail.html"
    pk_url_kwarg = "id"
    model = Book
    context_object_name = 'book'


# class BookDetailView(View):
#     template_name = "books/book_detail.html"
#
#     def get(self, request, id):
#         book = Book.objects.get(id=id)
#         return render(request, self.template_name, {"book": book})
