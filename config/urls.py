from django.contrib import admin
from django.urls import path, include
from advertisements.views import HomePageView

urlpatterns = [
    path(
        "admin/",
        admin.site.urls
    ),
    path(
        "",
        HomePageView.as_view(),
        name="home-page"
    ),
    path(
        "auth/",
        include(
            "django.contrib.auth.urls"
        )
    ),
    path(
        "",
        include(
            "advertisements.urls",
            namespace="advertisements"
        )
    ),
    path(
        "accounts/",
        include(
            "accounts.urls",
            namespace="accounts"
        )
    ),
    path(
        "category/",
        include(
            "categories.urls",
            namespace="categories"
        )
    ),
    path(
        "ratings/",
        include(
            "ratings.urls",
            namespace="ratings"
        )
    ),
]
