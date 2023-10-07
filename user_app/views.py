from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from .models import Profile, Patient,CustomUser 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, PatientForm, UpdateUserForm, ProfilePicForm, PatientDetailsForm
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth.models import User


def home1(request):
    template = loader.get_template('home1.html')
    return HttpResponse(template.render())

def home(request):
    user = request.user
    message = "You have logged in successfully." if user.is_authenticated else "Explore our features and start your journey towards a healthier life."
    context = {'user': user, 'message': message}
    return render(request, 'home.html', context)

def profile_list(request):
   if request.user.is_authenticated:
    profiles = Profile.objects.exclude(user=request.user)

    return render(request, 'profile_list.html', {"profiles":profiles}) 
   else:
    messages.success(request, "You Must be logged in to view this page...")
    return redirect('home')
   
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        
        return render(request, "profile.html", {"profile": profile})
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('home')
   
def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You Have Been Logged In!  "))
			return redirect('home')
		else:
			messages.success(request, ("There was an error logging in. Please Try Again..."))
			return redirect('login')

	else:
		return render(request, "login.html", {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You Have Been Logged Out. "))
	return redirect('home')

def register_user(request):
    # If the user is already authenticated, redirect to the home page
    if request.user.is_authenticated:
        return redirect('login')

    form = RegisterUserForm()
  

def register_user(request):
	form = RegisterUserForm()
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# first_name = form.cleaned_data['first_name']
			# second_name = form.cleaned_data['second_name']
			# email = form.cleaned_data['email']
			# Log in user
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("You have successfully registered! Welcome!"))
			return redirect('home')
	
	return render(request, "register_user.html", {'form':form})

def addPatient(request):
    submitted = False
    if request.method == "POST":
       form = PatientForm(request.POST)
       if form.is_valid():
          # Save the form and get the saved instance
          patient = form.save()
          # Access the patient's ID
          patient_id = patient.id
          # Redirect to showPatient with the patient's ID
          messages.success(request, f"You have Successfully registered {patient.firstName}.")

          return redirect('showPatient', patient_id)
    else:
          form = PatientForm()
          if 'submitted' in request.GET:
             submitted = True
    return render(request, 'addPatient.html', {'form': form, 'submitted': submitted})

def addPatientDetails(request, patient_id):
    submitted = False
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        form = PatientDetailsForm(request.POST)
        if form.is_valid():
            # Save the form and get the saved instance
            patient_details = form.save(commit=False)

            # Associate the patient details with the correct patient
            patient_details.patient = patient
            
            # Save the patient details
            patient_details.save()
            
            # Redirect to showPatient with the patient's ID
            messages.success(request, f"You have successfully saved the patient's health records.")
            return redirect('showPatient', patient_id)
    else:
        form = PatientDetailsForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'addPatientDetails.html', {'form': form, 'submitted': submitted, 'patient': patient})


def updatePatientDetails(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient_details = patient.patientdetails

    if request.method == 'POST':
        form = PatientDetailsForm(request.POST, instance=patient_details)
        if form.is_valid():
            form.save()
            messages.success(request, f"Successfully updated {patient.firstName}'s health records.")

            return redirect('addPatientDetails', patient_id=patient.id)

    else:
        form = PatientDetailsForm(instance=patient_details)

    return render(request, 'updatePatientDetails.html', {'form': form, 'patient': patient})

def listPatient(request):
    patientList = Patient.objects.all().order_by('-id')
    return render(request, 'patient.html', {'patientList': patientList})

def showPatient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    
    if request.method == "POST":
        action = request.POST.get('treat')
        
        if action == "untreat":
            request.user.profile.treats.remove(patient)
            messages.success(request, f"Successfully concluded treatment of {patient.firstName}.")
        elif action == "treat":
            request.user.profile.treats.add(patient)
            messages.success(request, f"Successfully began treatment of {patient.firstName}.")

    is_treated = patient in request.user.profile.treats.all()

    return render(request, 'showPatient.html', {'patient': patient, 'is_treated': is_treated})    
def showStaff(request):
    
    user = CustomUser.objects.get(pk=user_id)
    return render(request, 'profile.html', {'user': user})
      
def updateUser(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None,request.FILES or None, instance=profile_user)

        if request.method == 'POST':
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                profile_user.save()

                messages.success(request, "Your Profile has been updated")
                return redirect('home')

        return render(request, 'updateUser.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        messages.success(request, "You Must Be Logged in to See This Page")

        # Update the phone_number in the Profile model
        return redirect('home')   
