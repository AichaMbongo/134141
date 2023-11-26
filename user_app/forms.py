from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Patient, Profile, PatientDetails, DoctorPatientRel, Appointment, User, CustomUser, PatientVitals, DoctorReport, LabTest
from django.utils import timezone
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from datetime import date
import datetime




class OTPAuthenticationForm(AuthenticationForm):
    otp_code = forms.CharField(
        label="OTP Code",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

# class RegisterUserForm(UserCreationForm):
#     email = forms.EmailField()
#     first_name= forms.CharField( max_length=50)
#     last_name= forms.CharField( max_length=50)
   

#     class Meta:
#         model = User
#         fields =( 'username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        username = self.cleaned_data.get("username")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")

        # Check if password is too similar to personal information
        if password1.lower() in [username.lower(), first_name.lower(), last_name.lower()]:
            raise ValidationError(_("Your password can't be too similar to your other personal information."), code='password_too_similar')

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                raise ValidationError(_("The two password fields didn't match."), code='password_mismatch')

            # Check for additional constraints
            if len(password1) < 8:
                raise ValidationError(_("Your password must contain at least 8 characters."), code='password_too_short')

            if password1.isdigit():
                raise ValidationError(_("Your password can't be entirely numeric."), code='password_entirely_numeric')

            # Add more checks as needed

        return password2
    
    
    #create patient form
class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['firstName', 'lastName', 'dob', 'email', 'phoneNo', 'sex']
        widgets = {
            'firstName': forms.TextInput(attrs={'class':'form-control'}),
            'lastName': forms.TextInput(attrs={'class':'form-control'}),
            # 'dob': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'phoneNo': forms.TextInput(attrs={'class':'form-control'}),
            'sex': forms.Select(attrs={'class':'form-control'}),            
        }


# class PatientDetailsForm(forms.ModelForm):
#     class Meta:
#         model = PatientDetails
#         fields = ['dob', 'cp', 'trestbps', 'chol', 'fps', 'restech', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target', 'dateModified' ]
#     widgets = {
#     'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#     'cp': forms.NumberInput(attrs={'class': 'form-control'}),
#     'trestbps': forms.NumberInput(attrs={'class': 'form-control'}),
#     'chol': forms.NumberInput(attrs={'class': 'form-control'}),
#     'fps': forms.Select(attrs={'class': 'form-control'}, choices=((True, 'True'), (False, 'False'))),
#     'restech': forms.NumberInput(attrs={'class': 'form-control'}),
#     'thalach': forms.NumberInput(attrs={'class': 'form-control'}),
#     'exang': forms.Select(attrs={'class': 'form-control'}, choices=((True, 'True'), (False, 'False'))),
#     'oldpeak': forms.NumberInput(attrs={'class': 'form-control'}),
#     'slope': forms.NumberInput(attrs={'class': 'form-control'}),
#     'ca': forms.NumberInput(attrs={'class': 'form-control'}),
#     'thal': forms.NumberInput(attrs={'class': 'form-control'}),
#     'target': forms.Select(attrs={'class': 'form-control'}, choices=((True, 'True'), (False, 'False'))),
# }

class VitalsForm(forms.ModelForm):
    class Meta:
        model = PatientVitals
        fields = ['temperature', 'blood_pressure', 'heart_rate', 'respiratory_rate']
        widgets = {
            'temperature': forms.NumberInput(attrs={'class': 'form-control'}),
            'blood_pressure': forms.NumberInput(attrs={'class': 'form-control'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'respiratory_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
    def clean_temperature(self):
        temperature = self.cleaned_data.get('temperature')
        if temperature is not None and (temperature < 30 or temperature > 42):
            raise forms.ValidationError("Temperature should be between 30°C and 42°C.")
        return temperature

    def clean_blood_pressure(self):
        blood_pressure = self.cleaned_data.get('blood_pressure')
        if blood_pressure is not None and (not isinstance(blood_pressure, (int, float)) or blood_pressure < 60 or blood_pressure > 220):
            raise forms.ValidationError("Blood pressure should be a numeric value between 60 mm Hg and 220 mm Hg.")
        return blood_pressure

    def clean_heart_rate(self):
        heart_rate = self.cleaned_data.get('heart_rate')
        if heart_rate is not None and (heart_rate < 40 or heart_rate > 200):
            raise forms.ValidationError("Heart rate should be between 40 bpm and 200 bpm.")
        return heart_rate

    def clean_respiratory_rate(self):
        respiratory_rate = self.cleaned_data.get('respiratory_rate')
        if respiratory_rate is not None and (respiratory_rate < 10 or respiratory_rate > 40):
            raise forms.ValidationError("Respiratory rate should be between 10 breaths/min and 40 breaths/min.")
        return respiratory_rate



class CommentsForm(forms.Form):
    doctor_comments = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label="Doctor's Comments")


class PredictionVariablesForm(forms.ModelForm):
    class Meta:
        model = PatientDetails

        fields = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        widgets = {
            'temperature': forms.NumberInput(attrs={'class': 'form-control'}),
            'blood_pressure': forms.NumberInput(attrs={'class': 'form-control'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'respiratory_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}, choices=((0, 'Female'), (1, 'Male'))),
            'cp': forms.NumberInput(attrs={'class': 'form-control'}),
            'trestbps': forms.NumberInput(attrs={'class': 'form-control'}),
            'chol': forms.NumberInput(attrs={'class': 'form-control'}),
            'fbs': forms.Select(attrs={'class': 'form-control'}, choices=((0, 'less than 120 mg/dl'), (1, 'more than 120 mg/dl'))),
            'restecg': forms.NumberInput(attrs={'class': 'form-control'}),
            'thalach': forms.NumberInput(attrs={'class': 'form-control'}),
            'exang': forms.Select(attrs={'class': 'form-control'}, choices=((0, 'Absence'), (1, 'Presence'))),
            'oldpeak': forms.NumberInput(attrs={'class': 'form-control'}),
            'slope': forms.NumberInput(attrs={'class': 'form-control'}),
            'ca': forms.NumberInput(attrs={'class': 'form-control'}),
            'thal': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.required = True


#     # Set an initial value for the dateModified field
#  # Set an initial value for the dateModified field
#             # Set initial value for dateModified
#             if 'dateModified' in self.fields:
#                 self.fields['dateModified'].disabled = True

#     def save(self, commit=True):
#         instance = super().save(commit=False)

#         # Set 'dateModified' field before saving
#         instance.dateModified = timezone.now()

#         if commit:
#             instance.save()

#         return instance


        



class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
   

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')       


class ProfilePicForm(forms.ModelForm):
    specialization = forms.CharField( max_length=100)
    phone_number = forms.CharField(max_length=13)
    profile_image = forms.ImageField(label="Profile Picture")
    
    class Meta:
        model = Profile
        fields = ('phone_number', 'specialization' ,'profile_image', )


# class DoctorPatientRelForm(forms.ModelForm):
#     class Meta:
#         model = DoctorPatientRel
#         fields = ['user', 'patient', 'start_date', 'end_date']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

# class DoctorPatientRelForm(forms.ModelForm):
#     class Meta:
#         model = DoctorPatientRel
#         fields = ['start_date', 'end_date']

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         instance.user = self.initial['user']  # Set the user from the form's initial data
#         instance.patient = self.initial['patient']  # Set the patient from the form's initial data

#         if commit:
#             instance.save()

#         return instance

class DoctorPatientRelForm(forms.ModelForm):
    class Meta:
        model = DoctorPatientRel
        fields = ['doctor', 'patient', 'start_date', 'end_date']

    def __init__(self, *args, user=None, patient=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields['doctor'].initial = user
        if patient:
            self.fields['patient'].initial = patient

        # Set initial value for start_date
        self.fields['start_date'].initial = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance

class TreatmentPlanForm(forms.Form):
    medications = forms.CharField(label='Medications', widget=forms.Textarea)
    lifestyle_changes = forms.CharField(label='Lifestyle Changes', widget=forms.Textarea)
    follow_up_date = forms.DateField(label='Follow-up Date')
    additional_notes = forms.CharField(label='Additional Notes', widget=forms.Textarea)

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'purpose']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the 'doctor' field with choices from users with the 'Doctor' role
        self.fields['doctor'].queryset = Profile.objects.filter(role='doctor')


class DoctorReportForm(forms.ModelForm):
    class Meta:
        model = DoctorReport
        fields = '__all__'
        widgets = {
            'report_text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
            'patient': forms.HiddenInput(),  # Hide patient field as it is not editable in the report form
            # Add widgets for other fields as needed
        }

class LabTestForm(forms.ModelForm):
    TEST_TYPE_CHOICES = [
        ('typeA', 'CVD prediction'),
        ('typeB', 'Vitals'),
        ('typeC', 'X-ray'),
        # Add more test types as needed
    ]

    PATIENT_STATUS_CHOICES = [
        ('awaiting', 'Awaiting Test'),
        ('completed', 'Test Completed'),
        ('noNeed', 'No need for test'),
    ]

    test_type = forms.ChoiceField(
        label='Test Type',
        choices=TEST_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    patient_name = forms.CharField(
        label='Patient Name',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    status = forms.ChoiceField(
        label='Status',
        choices=PATIENT_STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    # Add other fields as needed

    class Meta:
        model = LabTest
        fields = ['test_type', 'patient_name', 'status']  # Add other fields as needed