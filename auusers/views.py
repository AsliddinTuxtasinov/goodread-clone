from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import View

from auusers.forms import UserCreateForm
User = get_user_model()


class RegisterView(View):
    def get(self, request):
        create_form = UserCreateForm()
        context = {
            'form': create_form,
        }
        return render(request, "users/register.html", context)

    def post(self, request):  # create user account
        create_form = UserCreateForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect("auusers:login")
        context = {'form': create_form}
        return render(request, "users/register.html", context)


class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html")
