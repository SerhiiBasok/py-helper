from django.urls import path
from accounts.views import (
    LoginAccountView,
    ProfileView,
    UpdateProfileView,
    register_view,
    ServingProfileView,
    LogoutConfirmView,
)

app_name = "accounts"  # Роут на аккаунти

urlpatterns = [
    path(
        "register/",
        register_view,
        name="registration"
    ),
    path(
        "login/",
        LoginAccountView.as_view(),
        name="login"
    ),
    path(
        "logout/confirm/",
        LogoutConfirmView.as_view(),
        name="logout_confirm"
    ),
    path(
        "profile/<int:pk>/",
        ProfileView.as_view(),
        name="profile"
    ),
    path(
        "profile/<int:pk>/update/",
        UpdateProfileView.as_view(),
        name="profile-update"
    ),
    path(
        "profile/<int:pk>/servings/",
        ServingProfileView.as_view(),
        name="profile-serving",
    ),
]
