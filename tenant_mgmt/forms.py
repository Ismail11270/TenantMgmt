from django import forms
from .views import Property, Address

from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(label='Your name', max_length=100)
    last_name = forms.CharField(label='Your surname', max_length=100)
  
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']