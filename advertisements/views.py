from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DeleteView, UpdateView
from django.views import generic

from advertisements.forms import AdvertisementForm
from advertisements.models import Advertisement

# Вʼю на оголошення

# основна сторінка
class HomePageView(generic.ListView):
    model = Advertisement
    template_name = "advertisements/home_page.html"
    context_object_name = "advertisements"

    # квері для відображення всіх оголошень
    def get_queryset(self):
        return Advertisement.objects.all()


# список оголошень
class AdvertisementList(generic.ListView):
    model = Advertisement
    template_name = "advertisements/advertisement_list.html"
    context_object_name = "advertisements"


# оголошення
class ApplicationView(generic.ListView):
    model = Advertisement

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


