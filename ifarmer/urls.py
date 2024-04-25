from django.urls import path
from . import views


urlpatterns = [
    # path('', views.landing_page, name='landing_page'),
    path('', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('admin_registration/', views.admin_registration, name='admin_registration'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_farmer/', views.add_farmer, name='add_farmer'),
    # path('allocate_inputs/<int:farmer_id>/', views.allocate_inputs, name='allocate_inputs'),
    # path('predict_yield/<int:farmer_id>/', views.predict_yield, name='predict_yield'),
   
]