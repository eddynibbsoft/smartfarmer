"""
URL configuration for smartfarmer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from ifarmer import views
from ifarmer.views import upload_dataset
from ifarmer.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.landing_page, name='landing_page'),
    path('', views.admin_login, name='admin_login'),
    path('admin_registration/', views.admin_registration, name='admin_registration'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_farmer/', views.add_farmer, name='add_farmer'),
    path('show_farmers/', views.show_farmers, name='show_farmers'),
    path('edit_farmer/<int:farmer_id>/', views.edit_farmer, name='edit_farmer'),
    path('delete_farmer/<int:farmer_id>/', views.delete_farmer, name='delete_farmer'),
    path('cluster/', views.cluster_farmers, name='cluster_farmers'),
    path('cluster_results/', views.cluster_farmers, name='cluster_results'),
    path('upload/', upload_dataset, name='upload_dataset'),
    path('view-uploaded-datasets/', view_uploaded_datasets, name='view_uploaded_datasets'),
    path('dataset/<int:pk>/', dataset_detail, name='dataset_detail'),
    # path('dataset/create/', dataset_create, name='dataset_create'),
    path('dataset/<int:pk>/update/', dataset_update, name='dataset_update'),
    path('dataset/<int:pk>/delete/', dataset_delete, name='dataset_delete'),
    path('train_model/', train_model, name='train_model'),
    path('allocate_inputs/<int:farmer_id>/', views.allocate_inputs, name='allocate_inputs'),
    # path('predict_yield/<int:farmer_id>/', views.predict_yield, name='predict_yield'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('generate-excel/', views.generate_excel, name='generate_excel'),
]
