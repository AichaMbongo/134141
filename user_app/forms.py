from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

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



    

