from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import ListView
from .models import Issue, Property
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import admin_requred, manager_requred

# Create your views here.

def home(request):
    return render(request, 'tnt_mgmt/home.html')

@method_decorator([login_required, manager_requred], name='dispatch')
class IssuesListView(ListView):
    model = Issue
    template_name = 'tnt_mgmt/issues.html'
    context_object_name = 'issues'

@method_decorator([login_required, manager_requred], name='dispatch')
class PropertiesListView(ListView):
    model = Property
    template_name = 'tnt_mgmt/properties.html'
    context_object_name = 'properties'


@login_required
@manager_requred
def newProperty(request):
    return HttpResponse("ASD")
# def list_users(request):
#     context = {
#         'users': User.objects.all(),
#         'title_spec': 'Users'
#     }
#     return render(request, 'tnt_mgmt\list_users.html', context)
    