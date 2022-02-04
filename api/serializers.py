from rest_framework import serializers
from django.contrib.auth import get_user_model

from books.models import Book, BookReview
User = get_user_model()


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "email", "profile_picture")


class BookSerializers(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ("id", "title", "description", "isbn", "coover_picture")


class BookReviewSerializers(serializers.ModelSerializer):
    book = BookSerializers(read_only=True)
    user = UserSerializers(read_only=True)

    class Meta:
        model = BookReview
        fields = ("id", "comment", "stars_given", "book", "user")
