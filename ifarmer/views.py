from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AdminLoginForm, AdminRegistrationForm, FarmerForm, InputAllocationForm
from .models import Farmer, InputAllocation, YieldPrediction

def landing_page(request):
    return render(request, 'landing_page.html')

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            for field, error in form.errors.items():
                messages.error(request, f"{field}: {error}")
            messages.error(request, 'Invalid form submission.')
    else:
        form = AdminLoginForm()
    return render(request, 'admin_login.html', {'form': form})

def admin_registration(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_login')
    else:
        form = AdminRegistrationForm()
    return render(request, 'admin_registration.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required
def dashboard(request):
    username = request.user.username
    return render(request, 'dashboard.html', {'username': username})

def add_farmer(request):
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allocate_inputs')
    else:
        form = FarmerForm()
    return render(request, 'add_farmer.html', {'form': form})

def allocate_inputs(request, farmer_id):
    farmer = Farmer.objects.get(id=farmer_id)
    if request.method == 'POST':
        form = InputAllocationForm(request.POST)
        if form.is_valid():
            input_allocation = form.save(commit=False)
            input_allocation.farmer = farmer
            input_allocation.save()
            return redirect('input_allocation_success')
    else:
        form = InputAllocationForm()
    return render(request, 'allocate_inputs.html', {'form': form, 'farmer': farmer})

def predict_yield(request, farmer_id):
    farmer = Farmer.objects.get(id=farmer_id)
    predicted_yield = 1000  # Dummy value for demonstration
    yield_prediction = YieldPrediction.objects.create(farmer=farmer, predicted_yield=predicted_yield)
    return render(request, 'predict_yield.html', {'farmer': farmer, 'predicted_yield': predicted_yield})
