from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from .models import Profile, Patient,CustomUser 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, PatientForm
from django.http import HttpResponseRedirect

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
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.error(request, "There was an error logging in, please try again")
            return redirect('login')
    else:
        return render(request, 'login.html', {})
    

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Successful!")
            return redirect('home')
        # The else block should be at the same indentation level as the 'if form.is_valid():'
    else:
            form = RegisterUserForm()
    

    return render(request, 'register_user.html', {'form': form})

def addPatient(request):
    submitted = False
    if request.method == "POST":
       form = PatientForm(request.POST)
       if form.is_valid():
          form.save()
          return HttpResponseRedirect('/addPatient?submitted=True')
    else:
          form = PatientForm
          if 'submitted' in  request.GET:
             submitted = True
    return render(request, 'addPatient.html', {'form': form, 'submitted': submitted})


def listPatient(request):
    patientList = Patient.objects.all()
    return render(request, 'patient.html', {'patientList': patientList})

def showPatient(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    return render(request, 'showPatient.html', {'patient': patient})
    
def showStaff(request):
    
    user = CustomUser.objects.get(pk=user_id)
    return render(request, 'profile.html', {'user': user})
      