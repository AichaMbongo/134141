from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile, Patient,CustomUser 
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterUserForm, PatientForm, UpdateUserForm, ProfilePicForm, PatientDetailsForm, DoctorPatientRelForm, AppointmentForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from mlxtend.classifier import StackingCVClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from .HeartDiseasePredUsingML import X_train, y_train 
from django.utils.safestring import mark_safe
import joblib
from django.urls import reverse
from .forms import TreatmentPlanForm
from .models import TreatmentPlan, Appointment, PatientDetails, PredictionResult
from django.db.models import Count

from django.http import FileResponse
import io
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from .forms import HeartDiseasePredictionForm
import requests
from .models import HeartDiseasePrediction
import csv

# ... (other imports)

# Instantiate the base models
knn = KNeighborsClassifier(n_neighbors=10)
svc = SVC(kernel='rbf', C=2)

# Instantiate the StackingCVClassifier
scv = StackingCVClassifier(classifiers=[knn, svc], meta_classifier=svc, random_state=42)


# from .HeartDiseasePredUsingML import make_prediction




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
        # treats = profile.treats.all().order_by('-id')  # Reverse the queryset
        
        
                
        
        
        # return render(request, "profile.html", {"profile": profile, "treats": treats})
        return render(request, "profile.html", {"profile": profile})

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
    pass
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
        
    #     if action == "untreat":
    #         request.user.profile.treats.remove(patient)
    #         messages.success(request, f"Successfully concluded treatment of {patient.firstName}.")
    #     elif action == "treat":
    #         request.user.profile.treats.add(patient)
    #         messages.success(request, f"Successfully began treatment of {patient.firstName}.")

    # is_treated = patient in request.user.profile.treats.all()

    # return render(request, 'showPatient.html', {'patient': patient, 'is_treated': is_treated})   
    return render(request, 'showPatient.html', {'patient': patient})   


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


@login_required(login_url='login')
def make_appointment(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Save the appointment details to the patient's record
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()

            messages.success(request, 'Appointment successfully made!')
            
            # Generate the URL for the patient's detail page
            patient_detail_url = reverse('showPatient', kwargs={'patient_id': patient_id})
            return redirect(patient_detail_url)
    else:
        form = AppointmentForm()

    return render(request, 'make_appointment.html', {'form': form, 'patient': patient})


def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'appointment_list.html', {'appointments': appointments})



@login_required(login_url='login')
def view_assigned_patients(request):
    if request.user.profile.role == 'doctor':
        doctor_profile = request.user.profile
        assigned_patients = Appointment.objects.filter(doctor=doctor_profile)
        return render(request, 'view_assigned_patients.html', {'assigned_patients': assigned_patients})
    else:
        # Handle the case where the user is not a doctor
        return render(request, 'access_denied.html')
    
@login_required(login_url='login')    
def view_health_records(request, patient_id):
    try:
        patient_details = PatientDetails.objects.get(id=patient_id)
    except PatientDetails.DoesNotExist:
        patient_details = None
    else:
        form = PatientDetailsForm()

    return render(request, 'view_health_records.html', {'patient_details': patient_details, 'form':form})






@login_required(login_url='login')    
def view_health_records(request, patient_id):
    try:
        patient_details = PatientDetails.objects.get(id=patient_id)
    except PatientDetails.DoesNotExist:
        patient_details = None
        form = PatientDetailsForm()  # Create an instance of the form
    else:
        form = None

    return render(request, 'view_health_records.html', {'patient_details': patient_details, 'form': form, 'patient_id': patient_id})



@login_required(login_url='login')    
def predict_health_records(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient_details = patient.patientdetails

    def generate_result_message(data):
        exang_result = "Present \nIndicates chest discomfort during exercise, potentially requiring attention." if data['arg_exang'] == 1 else "Absent \nPositive sign, suggesting the patient can \nengage in physical activity without \nchest discomfort"
        oldpeak_result = "No unusual change during exercise, a good sign." if data['arg_oldpeak'] == 0 else "Elevated. \nIndicates some changes, may need \ncloser examination for optimal heart health."
        slope_result = {
            1: "Upsloping: \nUsually a good sign.",
            2: "Flat: \nMay need further checking.",
            3: "Downsloping: \nMight indicate potential issues, needs careful evaluation for a healthy heart."
        }.get(data['arg_slope'], "Unknown Slope")

        ca_result = {
            0: "0: \nIndicates potential issues, needs careful \nevaluation for a healthy heart.",
            1: "1: \nIndicates potential issues, needs careful \nevaluation for a healthy heart.",
            2: "1: \nHigh blood vessel count observed, considered \na positive indicator for heart health.",
            3: "1: \nHigh blood vessel count observed, considered \na positive indicator for heart health."
        }.get(data['arg_ca'], "Unknown CA")

        cp_result = {
            1: "1. \nAtypical Angina:\n- What it Means: Different kind of chest pain.\n- What to Know: Might suggest a heart issue, needs checking.",
            2: "2. \nNon-Anginal Pain:\n- What it Means: Chest pain not related to the heart.\n- What to Know: Investigate to find out \nwhy you're feeling discomfort.",
            3: "3. \nAsymptomatic:\n- What it Means: No chest pain.\n- What to Know: Generally good, \nbut it's important to check everything \n just in case."
        }.get(data['arg_cp'], "Unknown CP")

        # Convert 'arg_trestbps' to an integer
        trestbps_value = int(data['arg_trestbps'])

        # Compare the integer value
        trestbps_result = "Higher than 125mm Hg \nblood pressure not within the \nnormal range is associated with \nhigher risks of cardiovascular diseases. \nCheck everything just in case." if trestbps_value > 125 else "Within the normal range. \nGood indicator of heart health."
        chol_result = {
            "Normal": "Within the normal range. \nGood indicator of heart health",
            "Borderline": "Borderline high. \nRisk for heart issues",
            "High": "High. \nRisk for heart issues"
        }.get(get_chol_category(data['arg_chol']), "Unknown Cholesterol")

        fbs_result = "Normal Level. \nIndicator of good heart health" if int(data['arg_fbs']) <= 120 else "Elevated Level. \nIndicates elevated blood sugar. Elevated levels may relate to conditions like diabetes, affecting heart health."

        restecg_result = "Abnormal Results (1 and 2): \nMay signal potential issues" if data['arg_restecg'] in [1, 2] else "Normal Results: \nPositive for heart health"

        thalach_result = "More than 140 \nmore likely to have heart disease." if data['arg_thalach'] > 140 else "Healthy range."

        target_result = "Low chance of heart attack" if data['target'] == 0 else "High chance of heart attack"

        result_message = [
            {'test': 'Exang', 'result': exang_result, 'purpose': 'tests for Exercise Induced Angina (pain \nin chest during exercise)'},
            {'test': 'Oldpeak', 'result': oldpeak_result, 'purpose': 'Measures how your heart\'s electrical \nactivity changes during exercise'},
            {'test': 'Slope', 'result': slope_result, 'purpose': 'Observes the pattern of the heart\'s \nelectrical activity during exercise'},
            {'test': 'CA', 'result': ca_result, 'purpose': 'Observes the Number of major vessels\n (0-3).  higher count for ca is \noften considered a positive indicator \nfor heart health'},
            {'test': 'CP', 'result': cp_result, 'purpose': 'Observes the Chest Pain type (0: \nTypical angina, 1: Atypical angina, \n2: Non-anginal pain, 3: Asymptomatic)'},
            {'test': 'Trestbps', 'result': trestbps_result, 'purpose': 'Observes the blood pressure. \nA healthy blood pressure reading is \ntypically less than 125 over 80'},
            {'test': 'Chol', 'result': chol_result, 'purpose': 'Observes the level of cholesterol in \nthe blood'},
            {'test': 'FBS', 'result': fbs_result, 'purpose': 'Observes the amount of glucose in \nyour blood after an overnight fast'},
            {'test': 'Restecg', 'result': restecg_result, 'purpose': 'Checks for Abnormalities like ST-T wave(1) \nor ventricular hypertrophy (2) suggest \nunderlying heart conditions needing further \ninvestigation or management'},
            {'test': 'Thalach', 'result': thalach_result, 'purpose': 'Checks for maximum heart rate achieved'},
            {'test': 'Prediction Outcome', 'result': target_result, 'purpose': 'Checks chances of getting \na heart attack'},
        ]

        return result_message

    def get_chol_category(chol_value):
        # Convert 'chol_value' to an integer
        chol_value_int = int(chol_value)
        if chol_value_int < 200:
            return "Normal"
        elif 200 <= chol_value <= 239:
            return "Borderline"
        else:
            return "High"

    if request.method == 'POST':
        form = PatientDetailsForm(request.POST, instance=patient_details)
        if form.is_valid():
            form_data = form.cleaned_data

            # Extract the features for prediction
            scv = joblib.load('C:/Users/HP/Desktop/test/134141/user_app/saved_model.sav')
            features_for_prediction = [
                form_data['arg_age'], form_data['arg_sex'], form_data['arg_cp'], form_data['arg_trestbps'], form_data['arg_chol'],
                form_data['arg_fbs'], form_data['arg_restecg'], form_data['arg_thalach'],
                form_data['arg_exang'], form_data['arg_oldpeak'], form_data['arg_slope'],
                form_data['arg_ca'], form_data['arg_thal']
            ]

            # Check if the StackingCVClassifier is fitted
            if not hasattr(scv, 'is_fitted') or not scv.is_fitted:
                # Fit the model with appropriate arguments
                # You may need to modify the fit arguments based on your model
                scv.fit(X_train, y_train)

            # Make the prediction using your model
            # Convert strings to numeric values
            features_for_prediction_numeric = [float(feature) for feature in features_for_prediction]

            # Make the prediction using your model
            prediction = scv.predict([features_for_prediction_numeric])[0]
            # prediction = scv.predict([features_for_prediction])[0]

            # Update the 'target' field with the prediction
            form_data['target'] = prediction

            # Determine the result_message based on the prediction
            result_message = generate_result_message(form_data)

            if prediction == 1:
                result_messages = f"{patient.firstName} has a high chance of experiencing a heart attack. Treatment should begin immediately."
                treatment_plan_url = reverse('treatment_plan', args=[patient.id])
                treatment_button = f'<a href="{treatment_plan_url}" class="btn btn-danger float-right">Fill Treatment Plan</a>'
                result_messages += f'<br/>{treatment_button}'
            else:
                result_message += f"{patient.firstName} has a low chance of experiencing a heart attack.<br/><br/> Ensure a healthy lifestyle is maintained and checkups are done yearly."
            messages.success(request, mark_safe(f" Prediction Outcome:<br/> {result_messages}"))
            # Render the result template with the detailed result message

            form.save()
             # Save each row of the table data into the PredictionResult model
            # Save each row of the table data into the PredictionResult model
            for result in result_message:
                PredictionResult.objects.create(
                    patient=patient,
                    test=result['test'],
                    result=result['result'],
                    purpose=result['purpose']
                )

          
            return render(request, 'patientPrediction.html', {'patient': patient, 'result_message': result_message})
        
      

    else:
        form = PatientDetailsForm(instance=patient_details)

    return render(request, 'predict_health_records.html', {'form': form})



def fill_patient_details(request, patient_id):
    try:
        patient_details = PatientDetails.objects.get(id=patient_id)
    except PatientDetails.DoesNotExist:
        patient_details = None

    if request.method == 'POST':
        form = PatientDetailsForm(request.POST)
        if form.is_valid():
            # Save the form data to the database or perform other actions
            # For example:
             patient_details = form.save(commit=False)
             patient_details.patient_id = patient_id
             patient_details.save()
            
        return redirect('view_health_records', patient_id=patient_id)
    else:
        form = PatientDetailsForm()

    return render(request, 'fill_patient_details.html', {'patient_details': patient_details, 'form': form, 'patient_id': patient_id})



@login_required(login_url='login')  
def index(request):
    # Role Distribution Data
    role_data = Profile.objects.values('role').annotate(count=Count('role'))
    role_labels = [entry['role'] for entry in role_data]
    role_count = [entry['count'] for entry in role_data]

    # Gender Distribution Data
    gender_data = Patient.objects.values('sex').annotate(count=Count('sex'))
    gender_labels = ['Male', 'Female']
    gender_count = [entry['count'] for entry in gender_data]


    # Data for Appointments per Day
    appointment_data = Appointment.objects.values('date').annotate(count=Count('date'))
    appointment_labels = [entry['date'].strftime('%Y-%m-%d') for entry in appointment_data]
    appointment_count = [entry['count'] for entry in appointment_data]


 
 # Last Login Distribution Data (for the last 7 days)
    last_login_data = User.objects.filter(last_login__gte=timezone.now() - timezone.timedelta(days=7))
    last_login_labels = [user.username for user in last_login_data]
    last_login_count = [1] * len(last_login_data)  # Assuming each login counts as 1


        # Gender Distribution Data
    gender_data = Patient.objects.values('sex').annotate(count=Count('sex'))
    gender_labels = ['Male Patient', 'Female Patient']
    gender_count = [entry['count'] for entry in gender_data]

    print("Gender Data:", gender_data)
    print("Gender Labels:", gender_labels)
    print("Gender Count:", gender_count)

    # Age Distribution data
    age_data = PatientDetails.objects.values_list('age', flat=True).exclude(age=None)
    age_labels = list(range(min(age_data), max(age_data) + 1))
    age_values = [age_data.count() for _ in age_labels]


    # Health Condition Distribution Data
    health_condition_data = PatientDetails.objects.values('target').annotate(count=Count('target'))
    health_condition_labels = ['Healthy', 'Not Healthy']
    health_condition_count = [entry['count'] for entry in health_condition_data]

    # User Status Distribution Data
    status_data = Profile.objects.values('on_leave').annotate(count=Count('on_leave'))
    status_labels = ['Not On Leave', ' On Leave']
    status_count = [entry['count'] for entry in status_data]

     # Doctor Specialization Distribution Data
    doctor_specialization_data = Profile.objects.filter(role='doctor', specialization__isnull=False).values('specialization').annotate(count=Count('specialization'))
    doctor_specialization_labels = [entry['specialization'] for entry in doctor_specialization_data]
    doctor_specialization_count = [entry['count'] for entry in doctor_specialization_data]




    return render(request, 'index.html', {
        'role_data': role_count,
        'role_labels': role_labels,
        'gender_data': gender_count,
        'gender_labels': gender_labels,
        'appointment_labels': appointment_labels,
        'appointment_data': appointment_count,
        'login_labels': last_login_labels,
        'login_data': last_login_count,
        'gender_data': gender_count,
        'gender_labels': gender_labels,
        'age_data': age_values,
        'age_labels': age_labels,
        'health_condition_data': health_condition_count,
        'health_condition_labels': health_condition_labels,
        'status_data': status_count,
        'status_labels': status_labels,
        'doctor_specialization_data': doctor_specialization_count,
        'doctor_specialization_labels': doctor_specialization_labels,
        })
def result_pdf(request):
    # Create a byte stream buffer
    buf = io.BytesIO()

    # Create a PDF document with the buffer
    pdf = SimpleDocTemplate(buf, pagesize=letter)

    # Designate the model
    results = PredictionResult.objects.all()[:11] 
 

    # Define styles for header, table, and text
    styles = getSampleStyleSheet()
    header_style = styles['Title']
    table_style = styles['BodyText']
    text_style = styles['Normal']

    # Generate header content
    patient_name = results.first().patient.firstName if results.exists() else "Unknown Patient"
    header_lines = [
        f"{patient_name}'s Prediction Results",
        f"Date: {results.first().date.strftime('%Y-%m-%d %H:%M:%S')}" if results.exists() else "No Date",
    ]

    # Generate table data
    table_data = [['Test', 'Result', 'Purpose']]
    table_data.extend([
        [result_instance.test, result_instance.result, result_instance.purpose]
        for result_instance in results
    ])

    # Create a table with appropriate styling
    table = Table(table_data, colWidths=[1.5 * inch, 2.9 * inch, 2.9 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
       ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add inner borders
    ]))

    # Build elements
    elements = []

    # Add header lines to the story
    for line in header_lines:
        elements.append(Paragraph(line, header_style))

    # Add an empty line before the table
    elements.append(Paragraph("<br/><br/>", text_style))

    # Add table to the story
    elements.append(table)

    # Build PDF document
    pdf.build(elements)

    # Reset buffer position
    buf.seek(0)


    return FileResponse(buf, as_attachment=True, filename='result_pdf.pdf')


def users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=users.csv'
    writer = csv.writer(response)
    users = User.objects.all()

    writer.writerow(['Username','First Name', 'Last Name', 'Email', 'Role', 'Phone Number', 'Date Joined', 'Last Login'])

    for user in users:
        writer.writerow([user.username, user.first_name, user.last_name, user.email, user.profile.role, user.profile.phone_number, user.date_joined, user.last_login])


    return response

def appointment_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=appointment.csv'
    writer = csv.writer(response)
    patients = Appointment.objects.all()

    writer.writerow(['Patient', 'Doctor', 'Date', 'Time', 'Purpose'])

    for patient in patients:
        writer.writerow([patient.patient, patient.doctor, patient.date, patient.time, patient.purpose])

    return response  # Move this line outside the for loop




def heart_disease_prediction(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient_details = patient.patientdetails
    form = HeartDiseasePredictionForm()

    if request.method == 'POST':
        form = HeartDiseasePredictionForm(request.POST, instance=patient_details)

        if form.is_valid():
            # Get form data
            form_data = form.cleaned_data

            # Set the API endpoint URL
            api_url = 'http://127.0.0.1:5022/target'

            # Make a GET request to the Plumber API
            response = requests.get(api_url, params=form_data)

            # Process the response
            if response.status_code == 200:
                data = response.json()

                # Create an instance of HeartDiseasePrediction model
                prediction_instance = HeartDiseasePrediction(
                    age=form_data['arg_age'],
                    sex=form_data['arg_sex'],
                    cp=form_data['arg_cp'],
                    trestbps=form_data['arg_trestbps'],
                    chol=form_data['arg_chol'],
                    fbs=form_data['arg_fbs'],
                    restecg=form_data['arg_restecg'],
                    thalach=form_data['arg_thalach'],
                    exang=form_data['arg_exang'],
                    oldpeak=form_data['arg_oldpeak'],
                    slope=form_data['arg_slope'],
                    ca=form_data['arg_ca'],
                    thal=form_data['arg_thal'],
                    prediction=data[0],  # Assuming the prediction is in the first element of data
                )

                # Save the instance to the database
                prediction_instance.save()

                # Fetch the saved instance from the database
                saved_instance = HeartDiseasePrediction.objects.get(id=prediction_instance.id)

                return render(
                        request,
                        'heart_disease_prediction.html',
                        { 'prediction_instance': saved_instance, 'form': form}
                    )            
            else:
                # Handle API error
                return render(request, 'heart_disease_prediction.html', {'error': 'API Error', 'form': form})

    return render(request, 'heart_disease_prediction.html', {'form': form})



    #        return render(request, 'patientPrediction.html', {'patient': patient, 'result_message': result_message})
        
      

    # else:
    #     form = PatientDetailsForm(instance=patient_details)

    # return render(request, 'predict_health_records.html', {'form': form})

