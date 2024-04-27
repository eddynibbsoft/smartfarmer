from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User  # Import Django's default User model
from .models import Farmer, InputAllocation
from django.contrib.postgres.fields import IntegerRangeField
from ifarmer import models

class FarmerForm(forms.ModelForm):
    
    VILLAGE_CHOICES = [(str(i), f"Village {i}") for i in range(1, 11)]  # Generate choices for villages 1 to 10
    
    REGION_CHOICES = [(str(x), f"Region {x}") for x in range(1, 6)]
    
    SOIL_TYPE_CHOICES = [
        ('Sandy Soil', 'Sandy Soil'),
        ('Black Clay', 'Black Clay'),
        ('Red Clay', 'Red Clay'),
        ('Alluvial Soil', 'Alluvial Soil'),
        ('Vlei Soil', 'Vlei Soil'),
        ('Saline Soil', 'Saline Soil'),
    ]

    LAND_SIZE_CHOICES = [
        (0, 'Less than 100'),
        (1, '100 - 500'),
        (2, '501 - 1000'),
        (3, '1001 - 5000'),
        (4, '5001 - 10000'),
        (5, 'Above 10 000'),
        # Add more choices as needed
    ]

    RAINFALL_CHOICES = [
       
        (1000, 'more than 1000mm per annum'),
        (950, '750 - 1000mm per annum'),
        (800, '650 - 800mm per annum'),
        (650, '450 - 650mm per annum'),
        (600, 'below 650mm per annum'),
        # Add more choices as needed
    ]

    address = forms.ChoiceField(choices=VILLAGE_CHOICES)
    region = forms.ChoiceField(choices=REGION_CHOICES)
    soil_type = forms.ChoiceField(choices=SOIL_TYPE_CHOICES)
    land_size = forms.ChoiceField(choices=LAND_SIZE_CHOICES)
    rainfall = forms.ChoiceField(choices=RAINFALL_CHOICES)

    class Meta:
        model = Farmer
        fields = ['full_name', 'region', 'land_size', 'crop_type', 'soil_type', 'rainfall', 'temperature', 'address', 'contact']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
# forms.py


class CustomAuthenticationForm(AuthenticationForm):
    # Add customizations if needed
    pass


class InputAllocationForm(forms.ModelForm):
    class Meta:
        model = InputAllocation
        fields = ['seeds', 'fertilizer', 'pesticides']