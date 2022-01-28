from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from auusers.forms import UserCreateForm, UserUpdateForm
User = get_user_model()


class RegisterView(View):
    template_name = "users/register.html"

    def get(self, request):
        create_form = UserCreateForm()
        context = {'form': create_form}
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request):
        create_form = UserCreateForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect("auusers:login")
        context = {'form': create_form}
        return render(request=request, template_name=self.template_name, context=context)


class LoginView(View):
    template_name = "users/login.html"

    def get(self, request):
        login_form = AuthenticationForm()
        return render(request=request, template_name=self.template_name, context={'login_form': login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request=request, user=user)
            messages.success(request, "you have successfuly logged in.")
            return redirect(to="books:books_list")
        return render(request=request, template_name=self.template_name, context={'login_form': login_form})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.info(request, "you have successfuly logged out.")
        return redirect(to="landing_page")


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "users/profile_page.html", {"user": request.user})


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user_update_form = UserUpdateForm(instance=request.user)
        return render(request, "users/profile_edit.html", {'form': user_update_form})

    def post(self, request):
        user_update_form = UserUpdateForm(instance=request.user, data=request.POST)
        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, "you have successfuly update profile")
            return redirect("auusers:profile")
        return render(request, "users/profile_edit.html", {'form': user_update_form})
