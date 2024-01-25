from django import forms
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.forms import PasswordInput

class RegistrationForm(forms.Form):
    """
    Represents a registration form.
    """
    first_name = forms.CharField(
        label='First Name',
        max_length=50,
        widget=forms.TextInput(attrs={"autocomplete": "off", "class": "form-control", "placeholder": "John", "aria-label": "First name"}),
        validators=[
            forms.validators.DataRequired(),
            forms.validators.RegexValidator('^[A-Za-z]*$', message='Only alphabetic characters are allowed.'),
        ]
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=50,
        widget=forms.TextInput(attrs={"autocomplete": "off", "class": "form-control", "placeholder": "Doe", "aria-label": "Last name"}),
        validators=[
            forms.validators.DataRequired(),
            forms.validators.RegexValidator('^[A-Za-z]*$', message='Only alphabetic characters are allowed.'),
        ]
    )
    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={"autocomplete": "off", "class": "form-control", "placeholder": "johndoe@example.com", "aria-label": "Email"}),
        validators=[
            forms.validators.DataRequired(),
            EmailValidator(),
        ]
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={"autocomplete": "off", "class": "form-control", "placeholder": "Password", "aria-label": "Password"}),
        validators=[
            forms.validators.DataRequired(),
            forms.validators.Length(min=8),
            RegexValidator('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]*$',
                           message='Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.'),
        ]
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={"autocomplete": "off", "class": "form-control", "placeholder": "Confirm password", "aria-label": "Confirm password"}),
        validators=[
            forms.validators.DataRequired(),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return confirm_password
