from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, DatasetForm, CustomAuthenticationForm, InputAllocationForm, FarmerForm
from .models import Farmer, Dataset
from collections import Counter
from sklearn.cluster import KMeans
import pandas as pd
from django.urls import reverse
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from django.http import JsonResponse
import json
import os
import joblib
import numpy as np


@login_required
def dashboard(request):
    # Get the username of the logged-in user
    username = request.user.username

    # Get the count of registered farmers
    num_registered_farmers = Farmer.objects.count()
    num_clusters = 10 
  

    # Render the dashboard template with the username and count of registered farmers
    return render(request, 'dashboard.html', {'username': username, 'num_registered_farmers': num_registered_farmers,  'num_clusters': num_clusters,})
# views.py


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
    farmer_data = [[farmer.address] for farmer in farmers]

    # Perform K-means clustering
    num_clusters = 10  # Assuming 10 villages
    kmeans = KMeans(n_clusters=num_clusters)
    cluster_labels = kmeans.fit_predict(farmer_data)

    # Group farmers by cluster label
    clustered_farmers = {}
    for idx, label in enumerate(cluster_labels):
        if label not in clustered_farmers:
            clustered_farmers[label] = []
        clustered_farmers[label].append(farmers[idx])

    # Pass clustering results to the template
    context = {
        'clustered_farmers': clustered_farmers,
        'num_clusters': num_clusters,  # Add the number of clusters to the context
    }
    return render(request, 'cluster_results.html', context)




def allocate_inputs(request, farmer_id):
    farmer = get_object_or_404(Farmer, pk=farmer_id)
    
    if request.method == 'POST':
        form = InputAllocationForm(request.POST)
        if form.is_valid():
            input_allocation = form.save(commit=False)
            input_allocation.farmer = farmer
            
            # Load the trained linear regression models
            models_dir = 'trained_models'
            input_allocation.seeds, input_allocation.fertilizer, input_allocation.pesticides = allocate_inputs_linear_regression(models_dir, farmer.land_size)
            
            input_allocation.save()
            return redirect('dashboard')  # Redirect to dashboard after successful allocation
    else:
        form = InputAllocationForm()
    
    return render(request, 'allocate_inputs.html', {'form': form, 'farmer': farmer})

def allocate_inputs_linear_regression(models_dir, land_size):
    seeds_model_path = os.path.join(models_dir, 'Seeds_model.pkl')
    fertilizer_model_path = os.path.join(models_dir, 'Fertilizer_model.pkl')
    pesticides_model_path = os.path.join(models_dir, 'Pesticides_model.pkl')
    
    # Load the trained linear regression models
    seeds_model = joblib.load(seeds_model_path)
    fertilizer_model = joblib.load(fertilizer_model_path)
    pesticides_model = joblib.load(pesticides_model_path)
    
    # Predict input allocation using the models
    seeds_allocation = seeds_model.predict([[land_size]])
    fertilizer_allocation = fertilizer_model.predict([[land_size]])
    pesticides_allocation = pesticides_model.predict([[land_size]])
    
    # You can round the allocations to integer values or apply any other post-processing
    return seeds_allocation, fertilizer_allocation, pesticides_allocation






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



def train_model(request):
    # Assuming you have logic to retrieve the dataset file path based on the dataset ID
    # For now, using a placeholder file path
    file_name = 'datasets/crop_dataset.csv'  # Specify the file path here
    
    try:
        # Read the dataset
        df = pd.read_csv(file_name)
    except Exception as e:
        return JsonResponse({'error': str(e)})  # Return error message if dataset loading fails
    
    # Define the crop type choices
    CROP_TYPE_CHOICES = [
        (115, 'Barley'),
        (1701, 'Beans, dry'),
        (1212, 'Cabbages'),
        (1251, 'Carrots and turnips'),
        (1610, 'Coffee, green'),
        (1706, 'Cow peas, dry'),
        (1232, 'Cucumbers and gherkins'),
        (1290, 'Green corn (maize)'),
        (142, 'Groundnuts, excluding shelled'),
        (112, 'Maize (corn)'),
        (118, 'Millet'),
        (117, 'Oats'),
        (1242, 'Peas, green'),
        (1651, 'Pepper (Piper spp.), raw'),
        (1510, 'Potatoes'),
        (113, 'Rice'),
        (141, 'Soya beans'),
        (1802, 'Sugar cane'),
        (1445, 'Sunflower seed'),
        (1530, 'Sweet potatoes'),
        (1620, 'Tea leaves'),
        (1234, 'Tomatoes'),
        (1970, 'Unmanufactured tobacco'),
        (111, 'wheat'),
    ]
    
    # Create a directory to save the trained models
    models_dir = 'trained_models'
    os.makedirs(models_dir, exist_ok=True)
    
    # Iterate over each crop type
    for crop_id, crop_type in CROP_TYPE_CHOICES:
        # Filter the dataset for the current crop type
        df_crop = df[df['crop_id'] == crop_id]
        
        # Data preprocessing
        X = df_crop[['land_size']]
        y = df_crop['input_allocation']
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Model training
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Save the trained model to disk
        model_file_path = os.path.join(models_dir, f'{crop_type}_model.pkl')
        joblib.dump(model, model_file_path)
    
    return JsonResponse({'message': 'Models trained and saved successfully.'})



def predict_inputs_allocation(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save()
            trained_model, score = train_model(dataset.id)
            # Now you can use trained_model for predictions
            # Example: prediction = trained_model.predict([[new_land_size, new_crop_type]])
            return redirect('view_uploaded_datasets')
    else:
        form = DatasetForm()
    return render(request, 'dataset_form.html', {'form': form})



def upload_dataset(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save()
            # Process the uploaded file
            process_dataset(dataset)
            return redirect(reverse('dashboard'))  # Redirect to admin dashboard
    else:
        form = DatasetForm()
    return render(request, 'upload_dataset.html', {'form': form})

def process_dataset(dataset):
    file_path = dataset.file.path
    # Assuming CSV file format
    df = pd.read_csv(file_path)
    # Process the DataFrame and save data to the database
    # Example: df.to_dict(), loop through the rows, and save each row as a model instance


def view_uploaded_datasets(request):
    # Retrieve the list of uploaded datasets from the database
    datasets = Dataset.objects.all()

    # Pass the datasets to the template for rendering
    context = {
        'datasets': datasets
    }
    return render(request, 'view_uploaded_datasets.html', context)

# def dataset_list(request):
#     datasets = Dataset.objects.all()
#     return render(request, 'dataset_list.html', {'datasets': datasets})

def dataset_detail(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    return render(request, 'dataset_detail.html', {'dataset': dataset})

# def dataset_create(request):
#     if request.method == 'POST':
#         form = DatasetForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('dataset_list')
#     else:
#         form = DatasetForm()
#     return render(request, 'dataset_form.html', {'form': form})

def dataset_update(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES, instance=dataset)
        if form.is_valid():
            form.save()
            return redirect('view_uploaded_datasets')
    else:
        form = DatasetForm(instance=dataset)
    return render(request, 'dataset_form.html', {'form': form})


def dataset_delete(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    if request.method == 'POST':
        dataset.delete()
        return redirect('view_uploaded_datasets')
    return render(request, 'dataset_confirm_delete.html', {'dataset': dataset})
