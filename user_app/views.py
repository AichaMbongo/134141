from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from .models import Profile
from django.contrib.auth import authenticate, login, logout

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def profile_list(request):
   if request.user.is_authenticated:
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'profile_list.html', {"profiles":profiles}) 
   else:
    messages.success(request, "You Must be logged in to view this page...")
    return redirect('home')
   
def login_user(request):
    return render(request, 'login.html', {}) 

      