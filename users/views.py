from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CreateUserForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth.decorators import login_required

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

@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def updateProfile(request):
    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account has been updated')
            return redirect('profile')

    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = UpdateProfileForm( instance=request.user.profile)



    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'users/update_profile.html', context)