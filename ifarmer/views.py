from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from .forms import AdminLoginForm, AdminRegistrationForm, FarmerForm, InputAllocationForm
from .forms import RegistrationForm
from .models import Farmer
from .forms import CustomAuthenticationForm



@login_required
def dashboard(request):
    # Get the username of the logged-in user
    username = request.user.username

    # Get the count of registered farmers
    num_registered_farmers = Farmer.objects.count()

    # Render the dashboard template with the username and count of registered farmers
    return render(request, 'dashboard.html', {'username': username, 'num_registered_farmers': num_registered_farmers})
# views.py

from django.shortcuts import render, redirect
from .forms import FarmerForm

def add_farmer(request):
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Assuming 'dashboard' is the name of your dashboard URL
    else:
        form = FarmerForm()
    return render(request, 'add_farmer.html', {'form': form})


@login_required
def show_farmers(request):
    farmers = Farmer.objects.all()
    return render(request, 'show_farmers.html', {'farmers': farmers})

@login_required
def edit_farmer(request, farmer_id):
    farmer = get_object_or_404(Farmer, pk=farmer_id)
    if request.method == 'POST':
        form = FarmerForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            return redirect('show_farmers')
    else:
        form = FarmerForm(instance=farmer)
    return render(request, 'edit_farmer.html', {'form': form})

@login_required
def delete_farmer(request, farmer_id):
    farmer = get_object_or_404(Farmer, pk=farmer_id)
    if request.method == 'POST':
        farmer.delete()
        return redirect('show_farmers')
    return render(request, 'confirm_delete_farmer.html', {'farmer': farmer})




# def allocate_inputs(request, farmer_id):
#     farmer = Farmer.objects.get(id=farmer_id)
#     if request.method == 'POST':
#         form = InputAllocationForm(request.POST)
#         if form.is_valid():
#             input_allocation = form.save(commit=False)
#             input_allocation.farmer = farmer
#             input_allocation.save()
#             return redirect('input_allocation_success')
#     else:
#         form = InputAllocationForm()
#     return render(request, 'allocate_inputs.html', {'form': form, 'farmer': farmer})

# def predict_yield(request, farmer_id):
#     farmer = Farmer.objects.get(id=farmer_id)
#     predicted_yield = 1000  # Dummy value for demonstration
#     yield_prediction = YieldPrediction.objects.create(farmer=farmer, predicted_yield=predicted_yield)
#     return render(request, 'predict_yield.html', {'farmer': farmer, 'predicted_yield': predicted_yield})

# views.py



def admin_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_login')
    else:
        form = RegistrationForm()
    return render(request, 'admin_registration.html', {'form': form})

# views.py


def admin_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard after login
    else:
        form = CustomAuthenticationForm()
    return render(request, 'admin_login.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('admin_login')