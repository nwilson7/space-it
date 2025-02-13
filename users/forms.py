from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'id': 'username-input'}),
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'id': 'email-input'}),
        required=True
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'password1-input'}),
        required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'password2-input'}),
        required=True
    )
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,  # Assuming your User model has a ROLE_CHOICES field
        widget=forms.Select(attrs={'id': 'role-select'}),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']


class UsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']