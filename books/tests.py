from django.test import TestCase
from django.urls import reverse

from books.models import Book


class BooksTestCase(TestCase):

    def test_no_books(self):
        response = self.client.get(path=reverse("books:books_list"))

        self.assertContains(response=response, text="Books not found.")

    def test_book_list_page(self):
        Book.objects.create(title="title1", description="description1", isbn="1111")
        Book.objects.create(title="title2", description="description2", isbn="2222")
        Book.objects.create(title="title3", description="description3", isbn="3333")

        books = Book.objects.all()
        response = self.client.get(path=reverse("books:books_list"))
        for book in books:
            self.assertContains(response=response, text=book.title)

    def test_book_detail_page(self):
        book = Book.objects.create(title="title1", description="description1", isbn="1111")
        response = self.client.get(path=reverse("books:book_detail", kwargs={"id": book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
