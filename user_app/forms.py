from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Patient

class OTPAuthenticationForm(AuthenticationForm):
    otp_code = forms.CharField(
        label="OTP Code",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    firstName= forms.CharField( max_length=50)
    lastName= forms.CharField( max_length=50)
    phoneNo= forms.CharField( max_length=13)

    class Meta:
        model = User
        fields =( 'username', 'firstName', 'lastName', 'phoneNo', 'email', 'password1', 'password2')


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

    

