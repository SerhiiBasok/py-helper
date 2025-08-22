from django.urls import path
from accounts.views import LoginAccountView, ProfileView

app_name = "accounts" #Роут на аккаунти

urlpatterns = [
    path("login/", LoginAccountView.as_view(), name="login" ),
    path("profile/", ProfileView.as_view(), name="profile"),

]
