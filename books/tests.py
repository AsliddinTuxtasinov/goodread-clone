from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from books.models import Book, Author, BookAuthor, BookReview
User = get_user_model()


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
        author1 = Author.objects.create(first_name="first_name1", last_name="last_name1",
                                        email="email1@gmail.com", bio="bio1")
        author2 = Author.objects.create(first_name="first_name2", last_name="last_name2",
                                        email="email2@gmail.com", bio="bio2")
        book_author1 = BookAuthor.objects.create(book=book, author=author1)
        book_author2 = BookAuthor.objects.create(book=book, author=author2)
        response = self.client.get(path=reverse("books:book_detail", kwargs={"id": book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
        self.assertContains(response, book_author1.author.full_name())
        self.assertContains(response, book_author2.author.full_name())

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


class BookReviewTestCase(TestCase):

    def setUp(self):
        self.book = Book.objects.create(title="title1", description="description1", isbn="1111")
        self.user = User.objects.create(username="asliddin", first_name="Asliddin",
                                        last_name="Tuxtasinov", email="asliddin@gmail.com")
        self.user.set_password("asliddin1!")
        self.user.save()
        BookReview.objects.create(user=self.user, book=self.book, comment="vala vala vala", stars_given=5)
        self.client.login(username="asliddin", password="asliddin1!")
        self.response = self.client.get(reverse("books:book_detail", kwargs={"id": self.book.id}))

    def test_add_review(self):
        self.response = self.client.post(
            path=reverse("books:add_review", kwargs={"id": self.book.id}),
            data={"comment": "Nice book", "stars_given": 3}
        )
        book_review = self.book.bookreview_set.last()

        self.assertEqual(self.book.bookreview_set.all().count(), 2)
        self.assertEqual(book_review.stars_given, 3)
        self.assertEqual(book_review.comment, "Nice book")
        self.assertEqual(book_review.book, self.book)
        self.assertEqual(book_review.user, self.user)
        self.assertEqual(self.response.url, reverse("books:book_detail", kwargs={"id": self.book.id}))

    def test_edit_review(self):
        book_review = self.book.bookreview_set.all()[0]

        self.assertEqual(BookReview.objects.count(), 1)
        self.assertContains(self.response, book_review.stars_given)
        self.assertContains(self.response, book_review.comment)

        self.response = self.client.post(
            path=reverse("books:edit_review", kwargs={"book_id": self.book.id, "review_id": book_review.id}),
            data={"comment": "good book", "stars_given": 1}
        )
        book_review = BookReview.objects.all()[0]

        self.assertEqual(self.response.url, reverse("books:book_detail", kwargs={"id": self.book.id}))
        self.assertNotEqual(book_review.stars_given, 3)
        self.assertNotEqual(book_review.comment, "Nice book")

        self.assertEqual(BookReview.objects.count(), 1)
        self.assertEqual(book_review.comment, "good book")

    def test_delete_review(self):
        book_review = self.book.bookreview_set.all()[0]

        self.assertEqual(BookReview.objects.count(), 1)
        self.assertContains(self.response, book_review.stars_given)
        self.assertContains(self.response, book_review.comment)

        self.response = self.client.get(
            reverse("books:delete_review", kwargs={"book_id": self.book.id, "review_id": book_review.id})
        )

        self.assertEqual(self.response.url, reverse("books:book_detail", kwargs={"id": self.book.id}))
        self.assertEqual(BookReview.objects.count(), 0)
