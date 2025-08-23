from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DeleteView, UpdateView
from django.views import generic

from advertisements.forms import AdvertisementForm
from advertisements.models import Advertisement, Application


# Вʼю на оголошення

# основна сторінка
class HomePageView(generic.ListView):
    model = Advertisement
    template_name = "advertisements/home_page.html"
    context_object_name = "advertisements"

    # квері для відображення всіх оголошень
    def get_queryset(self):
        return Advertisement.objects.filter(is_active=True).order_by('-created_at')


# список оголошень
class AdvertisementList(generic.ListView):
    model = Advertisement
    template_name = "advertisements/advertisement_list.html"
    context_object_name = "advertisements"
    paginate_by = 10


# оголошення
# class ApplicationView(generic.ListView):
#     model = Advertisement

# створення оголошення
class CreateAdvertisementView(generic.CreateView):
    model = Advertisement
    fields = ["title", "price", "location", "categories", "description"]
    template_name = "advertisements/advertisements_create.html"
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

#Оповертаю після створення оголошення в профіль де можна побачити та відреданувати
    def get_success_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.request.user.profile.pk})

# видалення оголошення
class DeleteAdvertisementView(DeleteView):
    model = Advertisement
    success_url = reverse_lazy("accounts:profile")

    # перенаправлення на профіль після видалення оголошення
    def get_success_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.request.user.profile.pk})

# редагування оголошення
class UpdateAdvertisementView(generic.UpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "advertisements/advertisements_update.html"

    def get_success_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.request.user.profile.pk})


def apply_to_advertisement(request, ad_pk):
    ad = get_object_or_404(Advertisement, pk=ad_pk)

    # перевіряємо, чи користувач вже подав заявку
    existing_app = Application.objects.filter(user=request.user, advertisement=ad).first()
    if not existing_app:
        Application.objects.create(
            user=request.user,
            advertisement=ad,
            message=f"{request.user.username} was send message"
        )

    return redirect("advertisements:list-advertisements")

@login_required
def reject_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if application.advertisement.user == request.user:
        application.delete()
    return redirect('accounts:profile-serving', pk=request.user.pk)

@login_required
def accept_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    ad = application.advertisement
    if ad.user == request.user:
        application.status = 'accepted'
        application.save()
        ad.is_active = False
        ad.save()
    return redirect('accounts:profile-serving', pk=request.user.pk)