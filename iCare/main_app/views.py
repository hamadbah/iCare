from django.shortcuts import render, redirect
# for login and sign up
from .forms import ProfileForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid signup - Please try again later'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def edit_profile(request):
    profile = request.user.profile
    
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'main_app/edit_profile.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'main_app/profile.html', {'profile': request.user.profile})