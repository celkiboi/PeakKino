from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User
from django.core.validators import MinValueValidator

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", required=True)

class RegistrationForm(UserCreationForm):
    age = forms.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        model = User
        fields = ['user_name', 'age', 'password1', 'password2']