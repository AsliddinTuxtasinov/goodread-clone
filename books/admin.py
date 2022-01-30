from django.contrib import admin
from books.models import Book, Author, BookAuthor, BookReview


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ("title", "isbn")
    list_display = ("title", "isbn")
    # list_filter = ("title", )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "last_name")
    list_display = ("first_name", "last_name", "email")


@admin.register(BookAuthor)
class BookAuthordmin(admin.ModelAdmin):
    search_fields = ("author", "author")
    list_display = ("book", "author")


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    search_fields = ("user", "book")
    list_display = ("user", "book", "stars_given")
