from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Address, Issue, Property, IssueCategory, Comment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import admin_requred, manager_requred, no_employee_allowed
from .forms import PropertyCreateForm, IssueCreateForm
from . import util
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.

def home(request):
    return render(request, 'tnt_mgmt/home.html')


class CustomUpdateView(UpdateView):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context


@method_decorator([login_required], name='dispatch')
class IssuesListView(ListView):
    model = Issue
    template_name = 'tnt_mgmt/issue/list.html'
    context_object_name = 'issues'
    paginate_by = 5

    def get_queryset(self):
        status = self.request.GET.get('status') 
        if status:
            if util.is_admin_or_manager(self.request.user):
                return Issue.objects.filter(status=status).order_by('-created')
            if util.is_employee(self.request.user):
                 return Issue.objects.filter(status=status, assignee=self.request.user)
        if util.is_admin_or_manager(self.request.user):
            return Issue.objects.all()
        if util.is_employee(self.request.user):
            return Issue.objects.filter(assignee=self.request.user)
        else:
            return Issue.objects.filter(submitter=self.request.user)

class IssuesForManagerListView(ListView):
    model = Issue
    template_name = 'tnt_mgmt/issue/list.html'
    context_object_name = 'issues'
    paginate_by = 5

    def get_queryset(self):
        status=self.kwargs.get('status')
        print(Issue.StatusENUM.choices)
        return Issue.objects.filter(status=Issue.StatusENUM.choices[status]).order_by('-created')
        # if util.is_admin_or_manager(self.request.user):
        #     return Issue.objects.all()
        # if util.is_employee(self.request.user):
        #     return Issue.objects.filter(assignee=self.request.user)
        # else:
        #     return Issue.objects.filter(submitter=self.request.user)


@method_decorator([login_required], name='dispatch')
class IssueDetailView(UserPassesTestMixin, DetailView):
    model = Issue
    template_name = 'tnt_mgmt/issue/detail.html'
    context_object_name = 'issue'
    ordering = ['dateAdded']

    def get_context_data(self, **kwargs):
        context = super(IssueDetailView, self).get_context_data(**kwargs)
        context['employees'] = User.objects.filter(groups__name='employee')
        return context

    def post(self, request, *args, **kwargs):
        issue = self.get_object()
        if request.method == 'POST':
            if request.POST['action'] == 'assign':
                employee = User.objects.get(id=request.POST['assignee'])
                issue.assignee = employee
                issue.manager = request.user
                issue.status = Issue.StatusENUM.ASS
                issue.save()
            elif request.POST['action'] == 'comment':
                comment = Comment(
                    messageText=request.POST['comment_text'], 
                    issue=issue, 
                    author=request.user
                )
                comment.save()
            elif request.POST['action'] == 'setStatus':
                issue.status = request.POST['status']
                issue.save()
        emps = User.objects.filter(groups__name='employee')
        return render(request,self.template_name, {'issue':issue, 'employees': emps})

    def test_func(self):
        issue = self.get_object()
        return util.is_admin_or_manager(self.request.user) or self.request.user == issue.submitter or self.request.user == issue.assignee


@method_decorator([login_required], name='dispatch')
class IssueUpdateView(UserPassesTestMixin, CustomUpdateView):
    model = Issue
    fields = ['title', 'description', 'category']
    template_name = 'tnt_mgmt/issue/form.html'

    def test_func(self):
        issue = self.get_object()
        return util.is_admin_or_manager(self.request.user) or self.request.user == issue.submitter

@login_required
@no_employee_allowed
def newIssue(request):
    if request.method == 'POST':
        form = IssueCreateForm(request.user, request.POST)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.submitter = request.user
            prop.save()
            return redirect('issueDetails', pk = prop.id) 
    else:
        form = IssueCreateForm(user = request.user)
    return render(request, 'tnt_mgmt/issue/form.html', {'form' : form })


@method_decorator([login_required, manager_requred], name='dispatch')
class PropertiesListView(ListView):
    model = Property
    template_name = 'tnt_mgmt/property/list.html'
    context_object_name = 'properties'
    paginate_by = 5


@method_decorator([login_required, manager_requred], name='dispatch')
class PropertyDetailView(DetailView):
    model = Property
    template_name = 'tnt_mgmt/property/detail.html'
    context_object_name = 'property'
    ordering = ['dateAdded']


@method_decorator([login_required, manager_requred], name='dispatch')
class PropertyUpdateView(CustomUpdateView):
    model = Property
    fields = ['name', 'owner', 'address']
    template_name = 'tnt_mgmt/property/form.html'


@method_decorator([login_required, manager_requred], name='dispatch')
class AddressListView(ListView):
    model = Address
    template_name = 'tnt_mgmt/address/list.html'
    context_object_name = 'addresses'
    paginate_by = 5

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


@method_decorator([login_required, manager_requred], name='dispatch')
class AddressUpdateView(CustomUpdateView):
    model = Address
    fields = ['country', 'city', 'zipCode', 'street', 'apartment']
    template_name = 'tnt_mgmt/address/form.html'


@method_decorator([login_required, manager_requred], name='dispatch')
class AddressDeleteView(DeleteView):
    model = Address
    template_name = 'tnt_mgmt/address/delete_confirm.html'
    def get_success_url(self) -> str:
        return reverse('addresses')


@method_decorator([login_required, admin_requred], name='dispatch')
class IssueCategoryDeleteView(DeleteView):
    model = IssueCategory
    template_name = 'tnt_mgmt/category/delete_confirm.html'

    def get_success_url(self) -> str:
        return reverse('categories')


@method_decorator([login_required, manager_requred], name='dispatch')
class PropertyDeleteView(DeleteView):
    model = Property
    template_name = 'tnt_mgmt/property/delete_confirm.html'
    def get_success_url(self) -> str:
        return reverse('addresses')

@method_decorator([login_required, manager_requred], name='dispatch')
class IssueDeleteView(DeleteView):
    model = Issue
    template_name = 'tnt_mgmt/issue/delete_confirm.html'
    def get_success_url(self) -> str:
        return reverse('issues')
    

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

@method_decorator([login_required, admin_requred], name='dispatch')
class IssueCategoryListView(ListView):
    model = IssueCategory
    template_name = 'tnt_mgmt/category/list.html'
    context_object_name = 'categories'
    ordering = ['dateAdded']
    paginate_by = 5

@method_decorator([login_required, admin_requred], name='dispatch')
class IssueCategoryCreateView(CreateView):
    model = IssueCategory
    template_name = 'tnt_mgmt/category/form.html'
    fields = ['title']


@method_decorator([login_required, admin_requred], name='dispatch')
class IssueCategoryUpdateView(CustomUpdateView):
    model = IssueCategory
    fields = ['title']
    template_name = 'tnt_mgmt/category/form.html'
    