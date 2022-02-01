from django import forms
from django.contrib.auth import get_user_model

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
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture')
