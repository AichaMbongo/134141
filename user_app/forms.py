from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Patient, Profile,  DoctorPatientRel, Appointment, User, CustomUser, HeartDiseasePrediction
from django.utils import timezone
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from datetime import date




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
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'phoneNo': forms.TextInput(attrs={'class':'form-control'}),
            'sex': forms.Select(attrs={'class':'form-control'}),            
        }

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 0:
                raise forms.ValidationError("Invalid date of birth")
            return age

    def save(self, commit=True):
        patient = super().save(commit=False)

        # Calculate age from date of birth
        dob = self.cleaned_data.get('dob')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 0:
                raise forms.ValidationError("Invalid date of birth")

            # Save age to PatientDetails
            patient_details, created = PatientDetails.objects.get_or_create(patient=patient)
            patient_details.age = age
            patient_details.save()

        if commit:
            patient.save()

        return patient
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

# class PatientDetailsForm(forms.ModelForm):
#     class Meta:
#         model = PatientDetails

#         fields = ['temperature', 'blood_pressure', 'heart_rate', 'respiratory_rate', 'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
#         widgets = {
#             'temperature': forms.NumberInput(attrs={'class': 'form-control'}),
#             'blood_pressure': forms.NumberInput(attrs={'class': 'form-control'}),
#             'heart_rate': forms.NumberInput(attrs={'class': 'form-control'}),
#             'respiratory_rate': forms.NumberInput(attrs={'class': 'form-control'}),
#             'age': forms.NumberInput(attrs={'class': 'form-control'}),
#             'sex': forms.Select(attrs={'class': 'form-control'}, choices=((0, 'Female'), (1, 'Male'))),
#             'cp': forms.NumberInput(attrs={'class': 'form-control'}),
#             'trestbps': forms.NumberInput(attrs={'class': 'form-control'}),
#             'chol': forms.NumberInput(attrs={'class': 'form-control'}),
#             'fbs': forms.Select(attrs={'class': 'form-control'}, choices=((0, 'less than 120 mg/dl'), (1, 'more than 120 mg/dl'))),
#             'restecg': forms.NumberInput(attrs={'class': 'form-control'}),
#             'thalach': forms.NumberInput(attrs={'class': 'form-control'}),
#             'exang': forms.Select(attrs={'class': 'form-control'}, choices=((0, 'Absence'), (1, 'Presence'))),
#             'oldpeak': forms.NumberInput(attrs={'class': 'form-control'}),
#             'slope': forms.NumberInput(attrs={'class': 'form-control'}),
#             'ca': forms.NumberInput(attrs={'class': 'form-control'}),
#             'thal': forms.NumberInput(attrs={'class': 'form-control'}),
#         }
    
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



class HeartDiseasePredictionForm(forms.Form):
    arg_age = forms.CharField(label='Age', widget=forms.TextInput(attrs={'class': 'form-control'}))
    arg_sex = forms.ChoiceField(label='Sex', choices=[(0, 'Female'), (1, 'Male')], widget=forms.Select(attrs={'class': 'form-control'}))
    arg_cp = forms.ChoiceField(label='Chest Pain Type', choices=[(0, 'Type 0'), (1, 'Type 1'), (2, 'Type 2'), (3, 'Type 3')], widget=forms.Select(attrs={'class': 'form-control'}))
    arg_trestbps = forms.CharField(label='Resting Blood Pressure', widget=forms.TextInput(attrs={'class': 'form-control'}))
    arg_chol = forms.CharField(label='Serum Cholesterol Level', widget=forms.TextInput(attrs={'class': 'form-control'}))
    arg_fbs = forms.ChoiceField(label='Fasting Blood Sugar', choices=[(0, 'No'), (1, 'Yes')], widget=forms.Select(attrs={'class': 'form-control'}))
    arg_restecg = forms.ChoiceField(label='Resting Electrocardiographic Results', choices=[(0, 'Type 0'), (1, 'Type 1'), (2, 'Type 2')], widget=forms.Select(attrs={'class': 'form-control'}))
    arg_thalach = forms.CharField(label='Maximum Heart Rate Achieved', widget=forms.TextInput(attrs={'class': 'form-control'}))
    arg_exang = forms.ChoiceField(label='Exercise-induced Angina', choices=[(0, 'No'), (1, 'Yes')], widget=forms.Select(attrs={'class': 'form-control'}))
    arg_oldpeak = forms.CharField(label='ST Depression Induced by Exercise Relative to Rest', widget=forms.TextInput(attrs={'class': 'form-control'}))
    arg_slope = forms.ChoiceField(label='Slope of the Peak Exercise ST Segment', choices=[(0, 'Type 0'), (1, 'Type 1'), (2, 'Type 2')], widget=forms.Select(attrs={'class': 'form-control'}))
    arg_ca = forms.CharField(label='Number of Major Vessels Colored by Fluoroscopy', widget=forms.TextInput(attrs={'class': 'form-control'}))
    arg_thal = forms.ChoiceField(label='Thalassemia Type', choices=[(0, 'Type 0'), (1, 'Type 1'), (2, 'Type 2'), (3, 'Type 3')], widget=forms.Select(attrs={'class': 'form-control'}))


class HeartDiseasePredictionForm(forms.ModelForm):
    class Meta:
        model = HeartDiseasePrediction
        # fields = '__all__'
        fields = ['age', 'sex','cp','trestbps','chol','fbs', 'restecg', 'thalach', 'exang','oldpeak', 'slope', 'ca','thal'   ]

        widgets = {
            'arg_age': forms.TextInput(attrs={'class': 'form-control'}),
            'arg_sex': forms.Select(attrs={'class': 'form-control'}),
            'arg_cp': forms.Select(attrs={'class': 'form-control'}),
            'arg_trestbps': forms.TextInput(attrs={'class': 'form-control'}),
            'arg_chol': forms.TextInput(attrs={'class': 'form-control'}),
            'arg_fbs': forms.Select(attrs={'class': 'form-control'}),
            'arg_restecg': forms.Select(attrs={'class': 'form-control'}),
            'arg_thalach': forms.TextInput(attrs={'class': 'form-control'}),
            'arg_exang': forms.Select(attrs={'class': 'form-control'}),
            'arg_oldpeak': forms.TextInput(attrs={'class': 'form-control'}),
            'arg_slope': forms.Select(attrs={'class': 'form-control'}),
            'arg_ca': forms.TextInput(attrs={'class': 'form-control'}),
            'arg_thal': forms.Select(attrs={'class': 'form-control'}),
        }

        # widgets = {
        #     'arg_age' : forms.CharField(label='Age', widget=forms.TextInput(attrs={'class': 'form-control'})),
        #     'arg_sex' : forms.ChoiceField(label='Sex', choices=[(0, 'Female'), (1, 'Male')], widget=forms.Select(attrs={'class': 'form-control'})),
        #     'arg_cp' : forms.ChoiceField(label='Chest Pain Type', choices=[(0, 'Type 0'), (1, 'Type 1'), (2, 'Type 2'), (3, 'Type 3')], widget=forms.Select(attrs={'class': 'form-control'})),
        #     'arg_trestbps' : forms.CharField(label='Resting Blood Pressure', widget=forms.TextInput(attrs={'class': 'form-control'})),
        #     'arg_chol' : forms.CharField(label='Serum Cholesterol Level', widget=forms.TextInput(attrs={'class': 'form-control'})),
        #     'arg_fbs ': forms.ChoiceField(label='Fasting Blood Sugar', choices=[(0, 'No'), (1, 'Yes')], widget=forms.Select(attrs={'class': 'form-control'})),
        #     'arg_restecg' : forms.ChoiceField(label='Resting Electrocardiographic Results', choices=[(0, 'Type 0'), (1, 'Type 1'), (2, 'Type 2')], widget=forms.Select(attrs={'class': 'form-control'})),
        #     'arg_thalach' : forms.CharField(label='Maximum Heart Rate Achieved', widget=forms.TextInput(attrs={'class': 'form-control'})),
        #     'arg_exang' : forms.ChoiceField(label='Exercise-induced Angina', choices=[(0, 'No'), (1, 'Yes')], widget=forms.Select(attrs={'class': 'form-control'})),
        #     'arg_oldpeak ': forms.CharField(label='ST Depression Induced by Exercise Relative to Rest', widget=forms.TextInput(attrs={'class': 'form-control'})),
        #     'arg_slope' : forms.ChoiceField(label='Slope of the Peak Exercise ST Segment', choices=[(0, 'Type 0'), (1, 'Type 1'), (2, 'Type 2')], widget=forms.Select(attrs={'class': 'form-control'})),
        #     'arg_ca' : forms.CharField(label='Number of Major Vessels Colored by Fluoroscopy', widget=forms.TextInput(attrs={'class': 'form-control'})),
        #     'arg_thal ': forms.ChoiceField(label='Thalassemia Type', choices=[(0, 'Type 0'), (1, 'Type 1'), (2, 'Type 2'), (3, 'Type 3')], widget=forms.Select(attrs={'class': 'form-control'})),

            
        # }





