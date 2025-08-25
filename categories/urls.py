from django.urls import path
from categories.views import CategoryCreateView

app_name = "categories"  # Роут на категорії

urlpatterns = [
    path("create/", CategoryCreateView.as_view(), name="category-create"),
]
