from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    isbn = models.CharField(max_length=20)
    cover_picture = models.ImageField(default="default-book-picture.jpg", upload_to="picture/")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("books:book_detail", kwargs={"id": self.pk})


class Author(models.Model):
    author = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="author")
    add_news = models.TextField()

    def full_name(self):
        return self.author.get_full_name()

    def __str__(self):
        return self.full_name()

    def get_absolute_url(self):
        return reverse("auusers:profile-author", kwargs={"id": self.pk})


class BookAuthor(models.Model):
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name="book_author")
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title} by {self.author}"


class BookReview(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    comment = models.TextField()
    stars_given = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.comment[:100]+'...'}"
