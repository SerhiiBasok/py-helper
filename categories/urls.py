from django.urls import path
from categories.views import CategoryListView

app_name = "categories" #Роут на категорії

urlpatterns = [
    path("category/", CategoryListView.as_view(), name="category-list" ),

]
