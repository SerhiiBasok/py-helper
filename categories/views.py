from django.shortcuts import render
from django.views.generic import ListView
from django.views import generic
from categories.models import Category

# Вʼю на категорії

class CategoryListView(generic.ListView):
    model = Category
    template_name = "categories/category_list.html"