from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views import generic
from categories.models import Category

# Вʼю на категорії

# категорії
class CategoryListView(generic.ListView):
    model = Category
    template_name = "categories/category_list.html"

#створення категорії
class CategoryCreateView(generic.CreateView):
    model = Category
    fields = "__all__"
    template_name = "categories/category_create.html"
    success_url = reverse_lazy("categories:category-list")
    context_object_name = "categories"
