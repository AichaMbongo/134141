from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
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
   
def profile (request, pk):
   if request.user.is_authenticated:
      profile = Profile.objects.get(user_id=pk)
      return render(request, "profile.html", {"profile": profile})
   else:
    messages.success(request, "You Must be logged in to view this page...")
    return redirect('home')

      
   
def login_user(request):
    if request.method == "POST":
       username = request.POST['username']
       password = request.POST['password']
       user = authenticate(request, username=username, password=password)
       if user is not None:
          login(request, user)
          messages.success(request, ("You have been logged in!"))
          return redirect('home')
       else:
           messages.success(request, ("There was an error logging in, please try again"))
           return redirect('login')
          
       
    else:
        return render(request, 'login.html', {}) 
    

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')

def register_user(request):
   return render(request, 'authenticate/register_user.html', {})

   

      