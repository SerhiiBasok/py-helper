from django.urls import path, include

from advertisements.views import (CreateAdvertisementView,
                                  DeleteAdvertisementView,
                                  UpdateAdvertisementView,
                                  AdvertisementList
                                  )

app_name = "advertisements" #Роут на основну сторінку з оголошеннями

urlpatterns = [
    path("adwcreate/", CreateAdvertisementView.as_view(), name="create-advertisement"),
    path("adwdelete/<int:pk>/", DeleteAdvertisementView.as_view(), name="delete-advertisement"),
    path("adwdelete/<int:pk>/update", UpdateAdvertisementView.as_view(), name="update-advertisement"),
    path("adwlist/", AdvertisementList.as_view(), name="list-advertisements"),


]
