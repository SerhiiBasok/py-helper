from django.urls import path
from accounts.views import LoginAccountView, ProfileView, UpdateProfileView, register_view

app_name = "accounts" #Роут на аккаунти

urlpatterns = [
    path("register/", register_view, name="registration"),
    path("login/", LoginAccountView.as_view(), name="login" ),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/update/", UpdateProfileView.as_view(), name="profile-update"),

]
