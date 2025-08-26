from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from accounts.models import Profile, User
from categories.models import Category


class ProfileLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        label="username",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username"
            }
        ),
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password"
            }
        )
    )



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            "username"
        ].widget.attrs.update({"class": "form-control"})
        self.fields[
            "password1"
        ].widget.attrs.update({"class": "form-control"})
        self.fields[
            "password2"
        ].widget.attrs.update({"class": "form-control"})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already registered.")
        return email


class ProfileForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    first_name = forms.CharField(
        max_length=150,
        required=False,
        label="First mame"
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label="Last name"
    )

    class Meta:
        model = Profile
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and not phone.isdigit():
            raise forms.ValidationError("Can be must only numbers")
        return phone

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        user = profile.user
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        if self.cleaned_data.get("categories"):
            profile.categories.set(self.cleaned_data["categories"])
        else:
            profile.categories.clear()

        return profile
