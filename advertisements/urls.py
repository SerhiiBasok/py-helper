from django.urls import path

from accounts.views import done_application
from advertisements.views import (
    CreateAdvertisementView,
    DeleteAdvertisementView,
    UpdateAdvertisementView,
    AdvertisementList,
    apply_to_advertisement,
    accept_application,
    reject_application,
)

app_name = "advertisements"

urlpatterns = [
    path
    ("adwcreate/",
     CreateAdvertisementView.as_view(),
     name="create-advertisement"
     ),
    path(
        "adwdelete/<int:pk>/",
        DeleteAdvertisementView.as_view(),
        name="delete-advertisement",
    ),
    path(
        "adwdelete/<int:pk>/update",
        UpdateAdvertisementView.as_view(),
        name="update-advertisement",
    ),
    path(
        "adwlist/",
        AdvertisementList.as_view(),
        name="list-advertisements"
    ),
    path(
        "advertisement/<int:ad_pk>/apply/",
        apply_to_advertisement, name="apply_to_ad"
    ),
    path(
        "application/<int:pk>/accept/",
        accept_application,
        name="accept_application"
    ),
    path(
        "application/<int:pk>/reject/",
        reject_application,
        name="reject_application"
    ),
    path(
        "application/<int:pk>/done/",
        done_application,
        name="done_application"
    ),
]
