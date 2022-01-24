from django.shortcuts import render
from django.views import View

from books.models import Book


class BooksView(View):
    template_name = "books/books_list.html"

    def get(self, request):
        books = Book.objects.all()
        return render(request=request, template_name=self.template_name, context={"books": books})


class BookDetailView(View):
    template_name = "books/book_detail.html"

    def get(self, request, id):
        book = Book.objects.get(id=id)
        return render(request, self.template_name, {"book": book})
