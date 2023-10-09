from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Patient, Profile, PatientDetails, DoctorPatientRel
from django.utils import timezone
from django.contrib.admin.widgets import AdminDateWidget



class OTPAuthenticationForm(AuthenticationForm):
    otp_code = forms.CharField(
        label="OTP Code",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name= forms.CharField( max_length=50)
    last_name= forms.CharField( max_length=50)
   

    class Meta:
        model = User
        fields =( 'username', 'first_name', 'last_name', 'email', 'password1', 'password2')


#create patient form
class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['firstName', 'lastName', 'email', 'phoneNo', 'sex']
        # labels = {
        #     'firstName': '',
        #     'lastName': '',
        #     'email': '',
        #     'phoneNo': '',
        #     'sex': '',            

        # }
        widgets = {
            'firstName': forms.TextInput(attrs={'class':'form-control'}),
            'lastName': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'phoneNo': forms.TextInput(attrs={'class':'form-control'}),
            'sex': forms.Select(attrs={'class':'form-control'}),            
        }

class PatientDetailsForm(forms.ModelForm):
    class Meta:
        model = PatientDetails
        fields = ['dob', 'cp', 'trestbps', 'chol', 'fps', 'restech', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target', 'dateModified' ]
    widgets = {
    'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    'cp': forms.NumberInput(attrs={'class': 'form-control'}),
    'trestbps': forms.NumberInput(attrs={'class': 'form-control'}),
    'chol': forms.NumberInput(attrs={'class': 'form-control'}),
    'fps': forms.Select(attrs={'class': 'form-control'}, choices=((True, 'True'), (False, 'False'))),
    'restech': forms.NumberInput(attrs={'class': 'form-control'}),
    'thalach': forms.NumberInput(attrs={'class': 'form-control'}),
    'exang': forms.Select(attrs={'class': 'form-control'}, choices=((True, 'True'), (False, 'False'))),
    'oldpeak': forms.NumberInput(attrs={'class': 'form-control'}),
    'slope': forms.NumberInput(attrs={'class': 'form-control'}),
    'ca': forms.NumberInput(attrs={'class': 'form-control'}),
    'thal': forms.NumberInput(attrs={'class': 'form-control'}),
    'target': forms.Select(attrs={'class': 'form-control'}, choices=((True, 'True'), (False, 'False'))),
}


   
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.required = True


    # Set an initial value for the dateModified field
 # Set an initial value for the dateModified field
            # Set initial value for dateModified
            if 'dateModified' in self.fields:
                self.fields['dateModified'].disabled = True

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Set 'dateModified' field before saving
        instance.dateModified = timezone.now()

        if commit:
            instance.save()

        return instance


        



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
