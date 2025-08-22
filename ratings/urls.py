from django.urls import path
from ratings.views import RatingListView

app_name = "ratings" #Роут на категорії

urlpatterns = [
    path("rating/", RatingListView.as_view(), name="rating-list" ),

]
