from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegistrationForm(UserCreationForm):
    """
    Custom registration form for user registration.

    Inherits from UserCreationForm and adds an email field.

    Attributes:
        email (forms.EmailField): Email field for the user.
    """
    email = forms.EmailField(max_length=255, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'address', 'phone_number']

class LoginForm(AuthenticationForm):
    """
    Custom login form for user authentication.

    Inherits from AuthenticationForm and modifies the fields to include an email field.

    Attributes:
        email (forms.EmailField): Email field for the user.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        """
        Initialize the login form.

        Removes the 'username' field from the form.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.
        """
        super().__init__(*args, **kwargs)
        del self.fields['username']