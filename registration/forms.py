from django_registration.forms import RegistrationForm
from registration.models import CustomUser
from django import forms


class CustomUserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]
