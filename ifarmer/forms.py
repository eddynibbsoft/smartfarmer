from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User  # Import Django's default User model
from .models import Farmer, InputAllocation

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['full_name', 'region', 'land_size', 'crop_type']

class InputAllocationForm(forms.ModelForm):
    class Meta:
        model = InputAllocation
        fields = ['water', 'fertilizer', 'pesticides']

class AdminRegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password confirmation")

    class Meta:
        model = User  # Use Django's default User model
        fields = ['username', 'email', 'password1', 'password2']

class AdminLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']
