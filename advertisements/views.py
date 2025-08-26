from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView
from django.views import generic
from advertisements.forms import AdvertisementForm
from advertisements.models import Advertisement, Application


class HomePageView(LoginRequiredMixin, generic.ListView):
    model = Advertisement
    template_name = "advertisements/home_page.html"
    context_object_name = "advertisements"

    def get_queryset(self):
        return Advertisement.objects.filter(
            is_active=True
        ).order_by(
            "-created_at"
        )[:3]


class AdvertisementList(LoginRequiredMixin, generic.ListView):
    model = Advertisement
    template_name = "advertisements/advertisement_list.html"
    context_object_name = "advertisements"
    paginate_by = 10

    def get_queryset(self):
        queryset = Advertisement.objects.filter(
            is_active=True
        ).order_by(
            "-created_at"
        )
        location = self.request.GET.get(
            "location"
        )
        category = self.request.GET.get(
            "category"
        )
        if location:
            queryset = queryset.filter(
                location__icontains=location
            )
        if category:
            queryset = queryset.filter(
                categories__name__icontains=category
            )
        return queryset


class CreateAdvertisementView(LoginRequiredMixin, generic.CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "advertisements/advertisements_create.html"
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "accounts:profile",
            kwargs={"pk": self.request.user.profile.pk}
        )


class DeleteAdvertisementView(LoginRequiredMixin, DeleteView):
    model = Advertisement

    def get_success_url(self):
        return reverse(
            "accounts:profile",
            kwargs={"pk": self.request.user.profile.pk}
        )


class UpdateAdvertisementView(
    LoginRequiredMixin,
    generic.UpdateView
):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "advertisements/advertisements_update.html"

    def get_success_url(self):
        return reverse(
            "accounts:profile",
            kwargs={"pk": self.request.user.profile.pk}
        )


@login_required
def apply_to_advertisement(request, ad_pk):
    ad = get_object_or_404(Advertisement, pk=ad_pk)
    existing_app = Application.objects.filter(
        user=request.user, advertisement=ad
    ).first()
    if not existing_app:
        Application.objects.create(
            user=request.user,
            advertisement=ad,
            message=f"{request.user.username} was send message",
        )

    return redirect("advertisements:list-advertisements")


@login_required
def reject_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if application.advertisement.user == request.user:
        application.delete()
    return redirect(
        "accounts:profile-serving",
        pk=request.user.pk
    )


@login_required
def accept_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    ad = application.advertisement
    if ad.user == request.user:
        application.status = "accepted"
        application.save()
        ad.is_active = False
        ad.save()
    return redirect(
        "accounts:profile-serving",
        pk=request.user.pk
    )
