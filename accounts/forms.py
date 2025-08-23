from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from accounts.models import Profile, User
from categories.models import Category


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
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # необов'язкове поле
    )

    class Meta:
        model = Profile
        exclude = ['user']

    # Валідація телефону
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and not phone.isdigit():
            raise forms.ValidationError("Телефон має містити лише цифри")
        return phone

    # Загальна валідація: хоча б телефон або біо
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

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
