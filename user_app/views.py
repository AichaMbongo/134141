from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from .models import Profile, Patient,CustomUser 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, PatientForm, UpdateUserForm, ProfilePicForm, PatientDetailsForm, DoctorPatientRelForm
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from allauth.account.decorators import verified_email_required
from allauth.account.models import EmailAddress
from .HeartDiseasePredUsingML import model
from mlxtend.classifier import StackingCVClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from .HeartDiseasePredUsingML import scv, X_train, y_train 
from django.utils.safestring import mark_safe
import joblib
from django.urls import reverse
from .forms import TreatmentPlanForm
from .models import TreatmentPlan
from django.utils.html import linebreaks
# ... (other imports)

# Instantiate the base models
knn = KNeighborsClassifier(n_neighbors=10)
svc = SVC(kernel='rbf', C=2)

# Instantiate the StackingCVClassifier
scv = StackingCVClassifier(classifiers=[knn, svc], meta_classifier=svc, random_state=42)


# from .HeartDiseasePredUsingML import make_prediction
import numpy as np




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
        treats = profile.treats.all().order_by('-id')  # Reverse the queryset
        
        
                
        
        
        return render(request, "profile.html", {"profile": profile, "treats": treats})
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('home')
   
# @login_required(login_url='login')
# @verified_email_required
# def login_user(request):
    # user = request.user
    # email_addresses = EmailAddress.objects.filter(user=user, verified=True)

    # # Check if the user has at least one verified email address
    # if not email_addresses.exists():
    #     # Redirect to the email verification page if no verified email
    #     return redirect('account_email_verification_sent')

    # # Check if the user has set up two-factor authentication
    # if not user.is_verified():
    #     # Redirect to the 2FA setup page if not set up
    #     return redirect('two_factor:setup')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There was an error logging in. Please Try Again...")
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
            login(request, user)
            messages.success(request, ("You have successfully registered! Welcome!"))
            return redirect('home')
        else:
            error_messages = []
            # Check for specific password constraints and append corresponding error messages
            if 'password1' in form.errors:
                error_messages.append("Your password can’t be too similar to your other personal information.")
            if 'password2' in form.errors:
                error_messages.append("Your password must contain at least 8 characters.")
            if 'password2' in form.errors:
                error_messages.append("Your password can’t be a commonly used password.")
            if 'password2' in form.errors:
                error_messages.append("Your password can’t be entirely numeric.")

            for message in error_messages:
                messages.error(request, message)

    return render(request, "register_user.html", {'form': form})

@login_required(login_url='login')
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


# @login_required(login_url='login')
# def addPatientDetails(request, patient_id):
#     submitted = False
#     patient = get_object_or_404(Patient, id=patient_id)

#     if request.method == "POST":
#         form = PatientDetailsForm(request.POST)
#         if form.is_valid():
#             # Save the form and get the saved instance
#             patient_details = form.save(commit=False)

#             # Associate the patient details with the correct patient
#             patient_details.patient = patient
            
#             # Save the patient details
#             patient_details.save()
            
#             # Redirect to showPatient with the patient's ID
#             messages.success(request, f"You have successfully saved the patient's health records.")
#             return redirect('showPatient', patient_id)
#     else:
#         form = PatientDetailsForm()
#         if 'submitted' in request.GET:
#             submitted = True

#     return render(request, 'addPatientDetails.html', {'form': form, 'submitted': submitted, 'patient': patient})



@login_required(login_url='login')
def addPatientDetails(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient_details = patient.patientdetails

    if request.method == 'POST':
        form = PatientDetailsForm(request.POST, instance=patient_details)
        if form.is_valid():
            # Get the form data
            form_data = form.cleaned_data

            # Extract the features for prediction
            scv = joblib.load('C:/Users/HP/Desktop/test/134141/user_app/saved_model.sav')
            features_for_prediction = [
                form_data['age'], form_data['sex'], form_data['cp'], form_data['trestbps'], form_data['chol'],
                form_data['fbs'], form_data['restecg'], form_data['thalach'],
                form_data['exang'], form_data['oldpeak'], form_data['slope'],
                form_data['ca'], form_data['thal']
            ]

            # Check if the StackingCVClassifier is fitted
            if not hasattr(scv, 'is_fitted') or not scv.is_fitted:
                # Fit the model with appropriate arguments
                # You may need to modify the fit arguments based on your model
                scv.fit(X_train, y_train)

            # Make the prediction using your model
            prediction = scv.predict([features_for_prediction])[0]

            # Update the 'target' field with the prediction
            form_data['target'] = prediction

            # Determine the result_message based on the prediction
            if prediction == 1:
                result_message = f"{patient.firstName} has a high chance of experiencing a heart attack. Treatment should begin immediately."
                
                # Generate the URL for the treatment plan form
                treatment_plan_url = reverse('treatment_plan', args=[patient.id])
                treatment_button = f'<a href="{treatment_plan_url}" class="btn btn-primary float-right">Fill Treatment Plan</a>'
                result_message += f'<br/>{treatment_button}'
            else:
                result_message = f"{patient.firstName} has a low chance of experiencing a heart attack.<br/><br/> Ensure a healthy lifestyle is maintained and checkups are done yearly."

            # Extracted features from the form data
            extracted_features = {
                # 'age': f'''<strong>{patient.firstName}'s Age - {form_data['age']} years old ''',
                # 'sex': f"<strong>{patient.firstName}'s Gender-  {form_data['sex']} <br/><br/> (1: Male, 0: Female)",
                'exang': f'''<strong>{patient.firstName}'s Exercise Induced Angina Result =  {form_data['exang']} <br/><br/> Explanation: <br/> (1: Presence, 0: Absence)
                            <br/>- Presence (1): Indicates chest discomfort during exercise, potentially requiring attention.
                            <br/>- Absence (0): Positive sign, suggesting the patient can engage in physical activity without chest discomfort.''', 

                'oldpeak': f'''<strong>{patient.firstName}'s heart behaviour during exercise Result: {form_data['oldpeak']} <br/><br/> Explanation: <br/>
                            - Measures how your heart's electrical activity changes during exercise.<br/> <br/> 
                            Effect on Heart Health:<br/> 

                            - Normal (0): No unusual change during exercise, a good sign. <br/> 
                           -  Elevated (>0): Indicates some changes, may need closer examination for optimal heart health. ''',
                'slope': f'''<strong>{patient.firstName}'s heart electrical activity during exercise. Result: {form_data['oldpeak']} <br/><br/> Explanation: <br/> 
                          - This is the pattern of the heart's electrical activity during exercise.<br/> <br/>
                          Effect on Heart Health:<br/> 

                        - Upsloping (1): Usually a good sign.<br/> 
                        - Flat (2): May need further checking.<br/> 
                        - Downsloping (3): Might indicate potential issues, needs careful evaluation for a healthy heart.''',


                'ca': f'''<strong>{patient.firstName}'s Number of Major Vessels =  {form_data['ca']} <br/><br/> Explanation: <br/>Number of major vessels (0-3)<br/>  
                            - A higher count for ca is often considered a positive indicator for heart health,<br/>
                            - A lower count may raise concerns about potential cardiovascular issues''',
                'cp': f'''<strong>{patient.firstName}'s Chest Pain Type =  {form_data['cp']} <br/><br/> Explanation: <br/> Chest Pain type (0: Typical angina, 
                            1: Atypical angina, 2: Non-anginal pain, 3: Asymptomatic). <br/> 1. Atypical Angina:<br/>
                                - What it Means: Different kind of chest pain. <br/>
                                - What to Know: Might suggest a heart issue, needs checking. <br/>
                                2. Non-Anginal Pain: <br/>
                                - What it Means: Chest pain not related to the heart. <br/>
                                - What to Know: Investigate to find out why you're feeling discomfort. <br/>

                                3. Asymptomatic: <br/>
                                - What it Means: No chest pain. <br/>
                                - What to Know: Generally good, but it's important to check everything just in case.''',
                'trestbps': f'''<strong>{patient.firstName}'s Resting blood pressure Result =   {form_data['trestbps']}<br/><br/> Explanation: <br/>
                                - A healthy blood pressure reading is typically less than 120 over 80. 
                            <br/>- This means your heart is doing well, pumping blood without putting too much pressure on your blood vessels.<br/>
                            - Higher than 125mm Hg blood pressure not within the normal range is associated with higher risks of cardiovascular diseases.
                              ''',
                'chol': f'''<strong>{patient.firstName}'s Cholesterol  fetched via BMI sensor =    {form_data['chol']} mg/dl <br/><br/> Explanation: <br/>
                        - What it Means: Level of fat in your blood.<br/>
                        - What to Know: Lower cholesterol is usually better for heart health. <br/>- High levels might indicate a risk for heart issues. Regular checkups help manage it.''',
                'fbs': f'''<strong>{patient.firstName}'s Fasting blood sugar Result =   {form_data['fbs']}  <br/><br/> Explanation: <br/> amount of glucose in your blood after an overnight fast.<br/>
                            -Normal Level (0): ≤120 mg/dl, considered normal.<br/>
                            Impact: Maintaining normal levels is crucial for overall health, including heart health.<br/><br/>
                            -Elevated Level (1): >120 mg/dl (1: True), indicates elevated blood sugar.<br/>
                            Impact: Elevated levels may relate to conditions like diabetes, affecting heart health. ''',
                
                'restecg': f'''<strong>{patient.firstName}'s Resting Electrocardiographic Results =  {form_data['restecg']} <br/><br/> Explanation: <br/>
                            - Normal Result (0): Positive for heart health.<br/>

                            Impact: Indicates healthy electrical activity within the heart.<br/><br/>
                            - Abnormal Results (1 and 2): May signal potential issues.<br/>

                            Impact: Abnormalities like ST-T wave (1) or ventricular hypertrophy (2) suggest underlying heart conditions needing further investigation or management. ''',
                'thalach': f'''<strong>{patient.firstName}'s highest heart rate during physical activity Result = {form_data['thalach']}<br/><br/> Explanation: <br/>
                - Higher maximum heart rates achieved indicate good heart health ''',
                'risk': f'''<strong>{patient.firstName}'s Risk of Heart Attack Result =  {form_data['target']} <br/> <br/> Explanation: <br/>
                        - 0:Indicates Less chance of heart attack <br/> 
                        - 1: More chance of heart attack <br/> 
                        '''
            }

            # Mapping of feature names to patient-friendly explanations
            feature_explanations = {
                # 'age': ''' ''',
                # 'sex': ''' ''',
                'exang': ''' ''',
                'oldpeak': ''' ''',  
                'slope': ''' ''', 
                'ca': ''' ''', 
                'cp': ''' ''',    
                'trestbps': ''' ''' ,             
                'chol': ''' ''',
                'fbs': '''
                           ''',
                'restecg': ''' ''',
                'thalach': ''' ''',
                'risk': ''' '''
            }

            # feature_explanations['age'] = linebreaks( feature_explanations['age'])
            # feature_explanations['sex'] = linebreaks(feature_explanations['sex'])
            feature_explanations['exang'] = linebreaks(feature_explanations['exang'])
            feature_explanations['oldpeak'] = linebreaks(feature_explanations['oldpeak'])
            feature_explanations['slope'] = linebreaks(feature_explanations['slope'])
            feature_explanations['ca'] = linebreaks(feature_explanations['ca'])
            feature_explanations['cp'] = linebreaks(feature_explanations['cp'])
            feature_explanations['trestbps'] = linebreaks(feature_explanations['trestbps'])
            feature_explanations['chol'] = linebreaks(feature_explanations['chol'])
            feature_explanations['fbs'] = linebreaks(feature_explanations['fbs'])
            feature_explanations['restecg'] = linebreaks(feature_explanations['restecg'])
            feature_explanations['thalach'] = linebreaks(feature_explanations['thalach'])
            feature_explanations['risk'] = linebreaks(feature_explanations['risk'])

            # Generate a summary message for the patient
            summary_message = "Based on the provided information:\n"
            for feature, value in extracted_features.items():
                explanation = feature_explanations.get(feature, 'Explanation not available')

            # Generate patient-friendly explanations
            explanations = {feature: f"{feature_explanations[feature]}: {extracted_features[feature]}" for feature in feature_explanations}

            # Save the updated form data to the database
            form.save()

            # Display the prediction result and accompanying statement
            messages.success(request, mark_safe(f" Prediction Outcome:<br/> {result_message}"))

            # Display the patient details and explanations in the template
            return render(request, 'patientPrediction.html', {'patient': patient, 'details': extracted_features, 'explanations': explanations})
    else:
        form = PatientDetailsForm(instance=patient_details)

    return render(request, 'updatePatientDetails.html', {'form': form, 'patient': patient})

from django.shortcuts import render, get_object_or_404


@login_required(login_url='login')
def patientPrediction(request, patient_id):
    if request.user.is_authenticated:
        # Assuming you have a Patient model and patient_id is passed in the URL
        patient = get_object_or_404(Patient, id=patient_id)

        # Pass the patient object to the template context
        return render(request, 'patientPrediction.html', {'patient': patient})
    else:
        messages.success(request, "You are not authenticated.")
        # Handle the case when the user is not authenticated
        # You might want to redirect or display an error message
        return HttpResponseRedirect('/login/')  # Redirect to login page, adjust the URL as needed



@login_required(login_url='login')
def treatment_plan(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = TreatmentPlanForm(request.POST)
        if form.is_valid():
            # Create a TreatmentPlan instance and associate it with the patient
            treatment_plan = TreatmentPlan(
                patient=patient,
                medications=form.cleaned_data['medications'],
                lifestyle_changes=form.cleaned_data['lifestyle_changes'],
                follow_up_date=form.cleaned_data['follow_up_date'],
                additional_notes=form.cleaned_data['additional_notes']
            )
            treatment_plan.save()
            return redirect('showPatient', patient_id=patient.id)

    else:
        form = TreatmentPlanForm()

    return render(request, 'treatment_plan.html', {'patient': patient, 'form': form})


@login_required(login_url='login')
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


@login_required(login_url='login')
def listPatient(request):
    patientList = Patient.objects.all().order_by('-id')
    return render(request, 'patient.html', {'patientList': patientList})

@login_required(login_url='login')
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


@login_required(login_url='login')
def showStaff(request):
    
    user = CustomUser.objects.get(pk=user_id)
    return render(request, 'profile.html', {'user': user})



@login_required(login_url='login')
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


# def ConfirmTreatment(request, patient_id):
#     if request.method == 'POST':
#         # Assuming you have a DoctorPatientRelForm that includes 'user' and 'patient' fields
#         form = DoctorPatientRelForm(request.POST)
#         if form.is_valid():
#             # Set the current user (doctor) in the form before saving
#             form.instance.user = request.user  # Assuming your user model is used for doctors
#             form.instance.patient_id = patient_id
#             form.save()
#             return redirect('showPatient')  # Redirect to a success page
#     else:
#         form = DoctorPatientRelForm()

#     return render(request, 'confirmTreatment.html', {'form': form})


# def ConfirmTreatment(request, patient_id):
#     patient = get_object_or_404(Patient, id=patient_id)

#     if request.method == 'POST':
#         form = DoctorPatientRelForm(request.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.doctor = request.user
#             instance.patient = patient
#             instance.start_date = timezone.now()
#             instance.save()
#             return redirect('showPatient')  
#     else:
#         initial_data = {'start_date': timezone.now().date()}  # Set initial data for start_date
#         form = DoctorPatientRelForm(initial=initial_data)

#     return render(request, 'confirmTreatment.html', {'form': form, 'patient': patient})

@login_required(login_url='login')
def ConfirmTreatment(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = DoctorPatientRelForm(request.POST, user=request.user, patient=patient)
        if form.is_valid():
            form.save()
            return redirect('showPatient', patient_id=patient.id)  # Redirect to a success page
    else:
        form = DoctorPatientRelForm(user=request.user, patient=patient)

    return render(request, 'confirmTreatment.html', {'form': form})