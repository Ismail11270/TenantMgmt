from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return render(request, 'tnt_mgmt\home.html')

# def list_users(request):
#     context = {
#         'users': User.objects.all(),
#         'title_spec': 'Users'
#     }
#     return render(request, 'tnt_mgmt\list_users.html', context)
    