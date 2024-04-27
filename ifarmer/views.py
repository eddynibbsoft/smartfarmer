from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm
from .models import Farmer
from .forms import CustomAuthenticationForm
from .forms import InputAllocationForm

from sklearn.cluster import KMeans


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

@login_required
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




def cluster_farmers(request):
    # Retrieve farmer data from the database
    farmers = Farmer.objects.all()
    farmer_data = [[farmer.land_size, farmer.address] for farmer in farmers]

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=10)  # Assuming 10 villages
    cluster_labels = kmeans.fit_predict(farmer_data)

    # Add cluster labels to farmer objects or store them separately
    for idx, farmer in enumerate(farmers):
        farmer.cluster_label = cluster_labels[idx]
        farmer.save()

    # Pass clustering results to the template
    context = {
        'farmers': farmers,
    }
    return render(request, 'cluster_results.html', context)


def allocate_inputs(request, farmer_id):
    farmer = get_object_or_404(Farmer, pk=farmer_id)
    
    if request.method == 'POST':
        form = InputAllocationForm(request.POST)
        if form.is_valid():
            input_allocation = form.save(commit=False)
            input_allocation.farmer = farmer
            
            # Implement input allocation logic based on land size
            if farmer.land_size < 10:
                input_allocation.seeds = 'Low'
                input_allocation.fertilizer = 'Low'
                input_allocation.pesticides = 'Low'
            elif 10 <= farmer.land_size < 20:
                input_allocation.seeds = 'Medium'
                input_allocation.fertilizer = 'Medium'
                input_allocation.pesticides = 'Medium'
            else:
                input_allocation.seeds = 'High'
                input_allocation.fertilizer = 'High'
                input_allocation.pesticides = 'High'
            
            input_allocation.save()
            return redirect('dashboard')  # Redirect to dashboard after successful allocation
    else:
        form = InputAllocationForm()
    
    return render(request, 'allocate_inputs.html', {'form': form, 'farmer': farmer})

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