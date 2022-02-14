from django.urls import path
from auusers import views


app_name = "auusers"

urlpatterns = [
    path('register', views.RegisterView.as_view(), name="register"),
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('profile', views.ProfileView.as_view(), name="profile"),
    path('profile/edit', views.ProfileUpdateView.as_view(), name="profile-edit"),
    path('profile/create/author/book', views.BookAuthorCreateView.as_view(), name="create-author-book"),
    path('profile/author/<int:id>', views.AuthorProfileView.as_view(), name="profile-author"),
]
