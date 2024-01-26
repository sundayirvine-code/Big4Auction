from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput
from .models import User
from django.contrib.auth import get_user_model

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'address', 'phone_number']

class LoginForm(AuthenticationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']