from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True,widget=TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(required=True, widget=PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields=['username', 'password']