from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

users = [
    {
        'username': 'Ismoil',
        'role': 'admin',
        'date_registered': 'Yesterday',
        'bio': 'I am an admin'
    },
    {
        'username': 'Brijesh',
        'role': 'tenant',
        'date_registered': 'Today',
        'bio': 'I just moved in'
    },
]

def home(request):
    return render(request, 'tnt_mgmt\home.html')

def list_users(request):
    context = {
        'users': users,
        'title_spec': 'Users'
    }
    return render(request, 'tnt_mgmt\list_users.html', context)
    