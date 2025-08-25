from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from accounts.forms import (ProfileForm,
                            CustomUserCreationForm,
                            ProfileLoginForm)
from accounts.models import Profile
from advertisements.models import Application


# Вʼю на account


# реєстрація користувача
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


# логін користувача
class LoginAccountView(LoginView):
    form_class = ProfileLoginForm
    template_name = "registration/login.html"


# вихід з системи
class LogoutConfirmView(View):
    template_name = "accounts/logged_out.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        logout(request)
        return redirect("login")


# Профіль користувача
class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = "accounts/profile.html"

    # оголошення користувача
    def get_queryset(self):
        return Profile.objects.select_related("user").prefetch_related(
            "user__advertisements"
        )

    # отримуємо або створюємо профіль користувача
    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )
        profile = Profile.objects.select_related("user").prefetch_related(
            "categories", "user__advertisements"
        ).get(
            pk=profile.pk
        )

        return profile


# оновлення користувача
class UpdateProfileView(LoginRequiredMixin,
                        generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/profile_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "accounts:profile",
            kwargs={
                "pk": self.object.user.pk
            }
        )


# лист бажаючих виконати завдання
class ServingProfileView(LoginRequiredMixin, generic.ListView):
    model = Application
    template_name = "accounts/servings.html"
    context_object_name = "applications"

    def get_queryset(self):
        return (
            Application.objects.filter(
                advertisement__user=self.request.user
            )
            .select_related(
                "user",
                "advertisement"
            )
            .order_by(
                "-created_at"
            )
        )


@login_required
def done_application(request, pk):
    application = get_object_or_404(
        Application.objects.select_related("advertisement"),
        pk=pk
    )
    ad = application.advertisement

    if ad.user == request.user and application.status == "accepted":
        ad.is_active = False
        ad.save()
        application.delete()

    return redirect("accounts:profile-serving", pk=request.user.pk)
