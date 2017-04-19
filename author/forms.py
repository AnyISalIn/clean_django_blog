from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from article.tools import get_field_attrs


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(get_field_attrs('Password')),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(get_field_attrs('Confirm Password')),
        strip=False,
        help_text='Enter the same password',
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(get_field_attrs('Username')),
            'email': forms.EmailInput(get_field_attrs('Email')),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            raise forms.ValidationError('A user with that email already exists.')
        self.instance.email = email
        return email


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(get_field_attrs('Username')),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(get_field_attrs('Password')),
    )
