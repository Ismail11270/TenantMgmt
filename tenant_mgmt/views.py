from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView
)

from .models import Address, Issue, Property
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import admin_requred, manager_requred
from .forms import PropertyCreateForm

# Create your views here.

def home(request):
    return render(request, 'tnt_mgmt/home.html')

@method_decorator([login_required, manager_requred], name='dispatch')
class IssuesListView(ListView):
    model = Issue
    template_name = 'tnt_mgmt/issue/list.html'
    context_object_name = 'issues'

@method_decorator([login_required, manager_requred], name='dispatch')
class PropertiesListView(ListView):
    model = Property
    template_name = 'tnt_mgmt/property/list.html'
    context_object_name = 'properties'

@method_decorator([login_required, manager_requred], name='dispatch')
class PropertyDetailView(DetailView):
    model = Property
    template_name = 'tnt_mgmt/property/detail.html'
    context_object_name = 'property'
    ordering = ['dateAdded']

@method_decorator([login_required, manager_requred], name='dispatch')
class AddressListView(ListView):
    model = Address
    template_name = 'tnt_mgmt/address/list.html'
    context_object_name = 'addresses'

@method_decorator([login_required, manager_requred], name='dispatch')
class AddressDetailView(DetailView):
    model = Address
    template_name = 'tnt_mgmt/address/detail.html'
    context_object_name = 'address'
    ordering = ['dateAdded']

@method_decorator([login_required, manager_requred], name='dispatch')
class AddressCreateView(CreateView):
    model = Address
    template_name = 'tnt_mgmt/address/form.html'
    fields = ['country', 'city', 'zipCode', 'street', 'apartment']

@login_required
@manager_requred
def newProperty(request):
    if request.method == 'POST':
        form = PropertyCreateForm(request.POST)
        if form.is_valid():
            prop = form.save()
            return redirect('propertyDetails', pk = prop.id) 
    else:
        form = PropertyCreateForm()
    return render(request, 'tnt_mgmt/property/form.html', {'form' : form })


# def list_users(request):

#     context = {
#         'users': User.objects.all(),
#         'title_spec': 'Users'
#     }
#     return render(request, 'tnt_mgmt\list_users.html', context)
    