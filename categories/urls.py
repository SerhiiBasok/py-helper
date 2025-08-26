from django.urls import path
from categories.views import CategoryCreateView

app_name = "categories"

urlpatterns = [
    path("create/", CategoryCreateView.as_view(), name="category-create"),
]
