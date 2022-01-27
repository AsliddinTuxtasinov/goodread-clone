from django.urls import path
from auusers.views import RegisterView, LoginView, ProfileView


app_name = "auusers"

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('profile', ProfileView.as_view(), name="profile"),
]
