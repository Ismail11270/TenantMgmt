from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from . import util
from .models import *

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(label='Your name', max_length=100)
    last_name = forms.CharField(label='Your surname', max_length=100)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class IssueCreateForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if util.is_admin_or_manager(user):
            return
        l = None
        if util.is_employee(user):
            properties = Property.objects.filter(assagnee=user)
        else:
            properties = Property.objects.filter(owner=user)
        choices = []
        for prop in properties:
            choices.append((prop.id, str(prop)),)
        self.fields['related_property'].choices = choices

    class Meta:
        model = Issue
        
        fields = '__all__'
        # widgets = {
        #     'email': forms.EmailField()
        # }
        exclude = ['assigner', 'assignee', 'submitter', 'status']
        # ass exclude in view.py before save/commit


class IssueCategoryCreateForm(ModelForm):

    class Meta:
        model = IssueCategory
        fields = '__all__'


class CommentsCreateForm(ModelForm):

    class Meta:
        model = Comments
        fields = ['messageText']


class AddressCreateForm(ModelForm):

    class Meta:
        model = Address
        fields = '__all__'


class PropertyCreateForm(ModelForm):

    class Meta:
        model = Property
        fields = '__all__'
        exclude = ['ownerId']
        # add ownerId from view



class IssueUpdateForm(ModelForm):

    class Meta:
        model = Issue
        fields = ['assigner', 'assignee']
        # ass exclude in view.py before save/commit