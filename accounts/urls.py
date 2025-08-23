from django.urls import path
from accounts.views import (LoginAccountView,
                            ProfileView,
                            UpdateProfileView,
                            register_view,
                            ServingProfileView)

app_name = "accounts" #Роут на аккаунти

urlpatterns = [
    path("register/", register_view, name="registration"),
    path("login/", LoginAccountView.as_view(), name="login" ),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/update/", UpdateProfileView.as_view(), name="profile-update"),
    path("profile/<int:pk>/servings/", ServingProfileView.as_view(), name="profile-serving"),

]
