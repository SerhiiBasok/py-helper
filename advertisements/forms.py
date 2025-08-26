from django import forms
from advertisements.models import Advertisement
from categories.models import Category


class AdvertisementForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Advertisement
        exclude = ["user"]
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 5, "class": "form-control form-control-lg"}
            ),
        }
