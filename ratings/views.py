from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, ListView
from accounts.models import Profile
from ratings.forms import FeedbackForm
from ratings.models import Rating


class UserInfoView(LoginRequiredMixin, ListView):
    model = Rating
    template_name = "ratings/user_rating.html"
    context_object_name = "ratings"

    def get_queryset(self):
        self.user_obj = get_object_or_404(
            Profile,
            user__id=self.kwargs["user_id"]
        ).user
        return (
            Rating.objects
            .filter(profile__user=self.user_obj)
            .select_related(
                "from_user",
                "profile",
                "profile__user"
            )
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_obj"] = self.user_obj
        profile = Profile.objects.select_related(
            "user"
        ).prefetch_related(
            "categories"
        ).get(user=self.user_obj)
        context["phone"] = profile.phone
        context["tags"] = [c.name for c in profile.categories.all()]

        from django.db.models import Avg
        avg_rating = Rating.objects.filter(
            profile=profile
        ).aggregate(Avg("rating"))["rating__avg"]
        context["avg_rating"] = avg_rating or 0

        return context


class MakeFeedback(LoginRequiredMixin, FormView):
    form_class = FeedbackForm
    template_name = "ratings/feedback.html"

    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(
            Profile,
            user__id=self.kwargs["user_id"]
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        Rating.objects.update_or_create(
            profile=self.profile,
            from_user=self.request.user,
            defaults={
                "rating": form.cleaned_data["rating"],
                "comment": form.cleaned_data["comment"],
            }
        )
        return redirect(
            "ratings:user-info",
            user_id=self.profile.user.id
        )
