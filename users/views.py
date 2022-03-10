from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CreateUserForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'You account was created successfully.')
            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'users/create_user.html', {'form': form})

def listUsers(request):
    context = {
        'users': User.objects.all(),
        'title_spec': 'Users'
    }
    return render(request, 'users/users_list.html', context)
