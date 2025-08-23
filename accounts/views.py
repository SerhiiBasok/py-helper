from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import FormView, UpdateView

from accounts.forms import ProfileForm, CustomUserCreationForm, ProfileLoginForm
from accounts.models import User, Profile


# Вʼю на account

#реєстрація користувача
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("accounts:profile", pk=user.profile.pk)
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

#логін користувача
class LoginAccountView(LoginView):
    form_class = ProfileLoginForm
    template_name = "registration/login.html"

#Профіль користувача
class ProfileView(generic.DetailView):
    model = Profile
    template_name = "accounts/profile.html"

    #оголошення користувача
    def get_queryset(self):
        return Profile.objects.select_related(
            "user"
        ).prefetch_related(
            "user__advertisements"
        )

    # отримуємо або створюємо профіль користувача
    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

# оновлення користувача
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/profile_update.html"

    def get_success_url(self):
        return reverse_lazy("accounts:profile", kwargs={"pk": self.object.pk})

