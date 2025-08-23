from django.urls import path
from categories.views import CategoryListView, CategoryCreateView

app_name = "categories" #Роут на категорії

urlpatterns = [
    path("list/", CategoryListView.as_view(), name="category-list" ),
    path("create/", CategoryCreateView.as_view(), name="category-create" ),

]
