from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from accounts.models import Profile, User

# форма реєстрації
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

# форма для редагування профілю
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = "__all__"

# форма логіну
class ProfileLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        label="username",
        widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
