from django.test import TestCase
from django.urls import reverse

from books.models import Book


class BooksTestCase(TestCase):

    def test_no_books(self):
        response = self.client.get(path=reverse("books:books_list"))
        self.assertContains(response=response, text="Books not found.")

    def test_book_list_page(self):
        book1 = Book.objects.create(title="title1", description="description1", isbn="1111")
        book2 = Book.objects.create(title="title2", description="description2", isbn="2222")
        book3 = Book.objects.create(title="title3", description="description3", isbn="3333")

        response = self.client.get(path=reverse("books:books_list") + "?page_size=2")
        for book in [book1, book2]:
            self.assertContains(response=response, text=book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(path=reverse("books:books_list") + "?page=2&page_size=2")
        self.assertContains(response=response, text=book3.title)

    def test_book_detail_page(self):
        book = Book.objects.create(title="title1", description="description1", isbn="1111")
        response = self.client.get(path=reverse("books:book_detail", kwargs={"id": book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_books(self):
        book1 = Book.objects.create(title="avatar", description="description1", isbn="1111")
        book2 = Book.objects.create(title="tom and jerry", description="description2", isbn="2222")
        book3 = Book.objects.create(title="nu pagadi", description="description3", isbn="3333")

        response = self.client.get(reverse("books:books_list") + "?q=and")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:books_list") + "?q=avatar")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:books_list") + "?q=pagadi")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)
