from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Patient, Profile, PatientDetails
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
# class SignUpForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
#     last_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')
#     email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
#     phone = forms.CharField(max_length=15, required=True, help_text='Required. Enter your phone number.')
#     specialization = forms.CharField(max_length=100, required=True, help_text='Required. Enter your specialization.')

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'specialization', 'password1', 'password2']


