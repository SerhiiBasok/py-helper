from django.views.generic import ListView
from django.views import generic
from advertisements.models import Advertisement

# Вʼю на оголошення

class HomePageView(generic.ListView):
    model = Advertisement
    template_name = "advertisements/home_page.html"

class ApplicationView(generic.ListView):
    model = Advertisement


