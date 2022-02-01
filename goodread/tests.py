from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from books.models import Book, BookReview
User = get_user_model()


class HomePageTestCase(TestCase):

    def test_paginated_list(self):
        book = Book.objects.create(title="title1", description="description1", isbn="1111")
        user = User.objects.create(username="asliddin", first_name="Asliddin",
                                   last_name="Tuxtasinov", email="asliddin@gmail.com")
        user.set_password("asliddin1!")
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=3, comment="Nice book, I recommend this")
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment="Good book")
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment="Awful bad book")

        response = self.client.get(reverse("home_page") + "?page_size=2")

        self.assertContains(response, review1.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review3.comment)
