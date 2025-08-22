from django.views import generic
from ratings.models import Rating


class RatingListView(generic.ListView):
    model = Rating
    template_name = "ratings/rating_list.html"