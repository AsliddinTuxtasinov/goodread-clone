from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from books.models import Book, BookReview
User = get_user_model()


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="asliddin", first_name="Asliddin",
                                        last_name="Tuxtasinov", email="asliddin@gmail.com")
        self.user.set_password("asliddin1!")
        self.user.save()
        self.book = Book.objects.create(title="title1", description="description1", isbn="1111")

        self.client.login(username="asliddin", password="asliddin1!")

    def test_book_review_detail_api(self):
        book_review = BookReview.objects.create(user=self.user, book=self.book, comment="vala vala vala", stars_given=5)

        response = self.client.get(reverse('api:review_detail', kwargs={'id': book_review.id}))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['id'], book_review.id)
        self.assertEqual(response.data['comment'], "vala vala vala")
        self.assertEqual(response.data['stars_given'], 5)

        self.assertEqual(response.data['book']['id'], book_review.book.id)
        self.assertEqual(response.data['book']['title'], "title1")
        self.assertEqual(response.data['book']['description'], "description1")
        self.assertEqual(response.data['book']['isbn'], "1111")

        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['username'], "asliddin")
        self.assertEqual(response.data['user']['first_name'], "Asliddin")
        self.assertEqual(response.data['user']['last_name'], "Tuxtasinov")
        self.assertEqual(response.data['user']['email'], "asliddin@gmail.com")

    def test_delete_book_review_api(self):
        book_review = BookReview.objects.create(user=self.user, book=self.book, comment="vala vala vala", stars_given=5)
        response = self.client.delete(reverse('api:review_detail', kwargs={'id': book_review.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=book_review.id).exists())

    def test_patch_book_review_api(self):
        book_review = BookReview.objects.create(user=self.user, book=self.book, comment="vala vala vala", stars_given=5)
        response = self.client.patch(reverse('api:review_detail', kwargs={'id': book_review.id}),
                                     data={"comment": "good books"})
        book_review.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["comment"], "good books")
        self.assertEqual(book_review.comment, "good books")

    def test_put_book_review_api(self):
        book_review = BookReview.objects.create(user=self.user, book=self.book, comment="vala vala vala", stars_given=5)
        response = self.client.put(reverse('api:review_detail', kwargs={'id': book_review.id}), data={
            "comment": "good books",
            "stars_given": 5,
            "book_id": self.book.id,
            "user_id": self.user.id
        })
        book_review.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["comment"], "good books")
        self.assertEqual(book_review.comment, "good books")
        self.assertEqual(response.data["stars_given"], 5)
        self.assertEqual(book_review.stars_given, 5)

    def test_create_book_review_api(self):
        data = {
            "comment": "I recommend to read this book",
            "stars_given": 5,
            "book_id": self.book.id,
            "user_id": self.user.id
        }
        response = self.client.post(path=reverse('api:reviews_list'), data=data)
        book_review = BookReview.objects.get(book=self.book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(book_review.stars_given, data["stars_given"])
        self.assertEqual(book_review.comment, data["comment"])


    def test_book_review_list_api(self):
        user2 = User.objects.create(username="cool", email="asliddin5@gmail.com")
        user2.set_password("cool1!")
        user2.save()

        book_review1 = BookReview.objects.create(user=self.user, book=self.book,
                                                 comment="vala vala vala", stars_given=5)
        book_review2 = BookReview.objects.create(user=user2, book=self.book, comment="dara dara dam", stars_given=3)

        response = self.client.get(reverse('api:reviews_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

        self.assertEqual(response.data['results'][0]['id'], book_review2.id)
        self.assertEqual(response.data['results'][0]['stars_given'], book_review2.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], book_review2.comment)

        self.assertEqual(response.data['results'][1]['id'], book_review1.id)
        self.assertEqual(response.data['results'][1]['stars_given'], book_review1.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], book_review1.comment)
