from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from categories.models import Category


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    fields = "__all__"
    template_name = "categories/category_create.html"
    success_url = reverse_lazy("categories:category-list")
    context_object_name = "categories"
