from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, ListView
from accounts.models import Profile
from ratings.forms import FeedbackForm
from ratings.models import Rating

 # відгуки та коментарі про юзера
class UserInfoView(LoginRequiredMixin, ListView):
    model = Rating
    template_name = "ratings/user_rating.html"
    context_object_name = "ratings"

    def get_queryset(self):
        self.user_obj = get_object_or_404(
            Profile,
            user__id=self.kwargs["user_id"]
        ).user
        return Rating.objects.filter(
            profile__user=self.user_obj
        ).order_by(
            "-created_at"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_obj"] = self.user_obj
        profile = self.user_obj.profile
        context["phone"] = profile.phone
        context["tags"] = [c.name for c in profile.categories.all()]
        avg = Rating.objects.filter(
            profile=profile
        ).aggregate(
            Avg(
                "rating"
            )
        )["rating__avg"]
        context["avg_rating"] = avg
        return context

# форма фідбеку
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
