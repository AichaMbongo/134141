from django import forms
from django.contrib.auth.forms import AuthenticationForm

class OTPAuthenticationForm(AuthenticationForm):
    otp_code = forms.CharField(
        label="OTP Code",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
