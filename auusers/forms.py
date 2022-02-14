from django import forms
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from books.models import Author, Book, BookAuthor

User = get_user_model()


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture', 'are_you_author')


class BookAuthorCreateForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea())
    isbn = forms.CharField(min_length=20)

    def save(self, request, validate_data):
        author = get_object_or_404(Author, author=request.user)
        book = Book.objects.create(**validate_data)
        BookAuthor.objects.create(author=author, book=book)
        print(validate_data)
        print(request.user)
