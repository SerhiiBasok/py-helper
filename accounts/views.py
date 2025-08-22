from django.contrib.auth.views import LoginView
from django.views import generic
from accounts.models import User, Profile


# Вʼю на логін

class LoginAccountView(LoginView):
    model = User
    template_name = "registration/login.html"

class ProfileView(generic.ListView):
    model = Profile
    template_name = "accounts/profile.html"