from django.urls import path
from . import views
from .views import show_farmers, edit_farmer, delete_farmer
from .views import upload_dataset

from .views import *

urlpatterns = [
    # Other URL patterns
   
]


urlpatterns = [
    # path('', views.landing_page, name='landing_page'),
    path('', admin_login, name='admin_login'),
    path('logout/', admin_logout, name='admin_logout'),
    path('admin_registration/', admin_registration, name='admin_registration'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add_farmer/', add_farmer, name='add_farmer'),
    path('show_farmers/', show_farmers, name='show_farmers'),
    path('edit_farmer/<int:farmer_id>/', edit_farmer, name='edit_farmer'),
    path('delete_farmer/<int:farmer_id>/', delete_farmer, name='delete_farmer'),
    path('cluster/', cluster_farmers, name='cluster_farmers'),
    path('cluster_results/', cluster_farmers, name='cluster_results'),
    path('upload/', upload_dataset, name='upload_dataset'),
    path('view-uploaded-datasets/', view_uploaded_datasets, name='view_uploaded_datasets'),
    path('dataset/<int:pk>/', dataset_detail, name='dataset_detail'),
    # path('dataset/create/', dataset_create, name='dataset_create'),
    path('dataset/<int:pk>/update/', dataset_update, name='dataset_update'),
    path('dataset/<int:pk>/delete/', dataset_delete, name='dataset_delete'),
    path('train_model/', train_model, name='train_model'),
    path('allocate_inputs/<int:farmer_id>/', allocate_inputs, name='allocate_inputs'),
    # path('predict_yield/<int:farmer_id>/', views.predict_yield, name='predict_yield'),
   
]