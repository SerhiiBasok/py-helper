from django.urls import path
from ratings.views import UserInfoView, MakeFeedback

app_name = "ratings"

urlpatterns = [
    path(
        "info<int:user_id>/",
        UserInfoView.as_view(),
        name="user-info"
    ),
    path(
        "feedback<int:user_id>/",
        MakeFeedback.as_view(),
        name="feedback"
    ),
]
