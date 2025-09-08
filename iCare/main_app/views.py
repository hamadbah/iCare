from django.shortcuts import render, redirect
# for login and sign up
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required # to secure pages only while required is valid
from django.contrib.auth.mixins import LoginRequiredMixin # to secure pages only while required is valid

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
            return redirect('index')
        else:
            error_message = 'Invalid signup - Please try again later'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)