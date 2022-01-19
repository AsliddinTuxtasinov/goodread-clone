from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    isbn = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BookAuthor(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title} by {self.author}"


class BookReview(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    comment = models.TextField()
    stars_given = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.user} - {self.comment}"
