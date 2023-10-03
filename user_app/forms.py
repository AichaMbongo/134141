from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Patient, Profile

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
    phone_number= forms.CharField( max_length=13)

    class Meta:
        model = User
        fields =( 'username', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2')


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


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=13)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'email')       


class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture")
    
    class Meta:
        model = Profile
        fields = ('profile_image', )
# class SignUpForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
#     last_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')
#     email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
#     phone = forms.CharField(max_length=15, required=True, help_text='Required. Enter your phone number.')
#     specialization = forms.CharField(max_length=100, required=True, help_text='Required. Enter your specialization.')

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'specialization', 'password1', 'password2']


