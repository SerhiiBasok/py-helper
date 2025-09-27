from django import forms
from django.forms import ModelForm
from ratings.models import Rating


class FeedbackForm(ModelForm):
    class Meta:
        model = Rating
        fields = ("rating", "comment")
        widgets = {
            "rating": forms.RadioSelect(choices=Rating.RATING_CHOICES),
            "comment": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Your comment",
                "class": "form-control"
            }),
        }
        labels = {
            "rating": "Rating",
            "comment": "Comment",
        }
