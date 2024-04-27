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
    path('allocate_inputs/<int:farmer_id>/', views.allocate_inputs, name='allocate_inputs'),
    # path('predict_yield/<int:farmer_id>/', views.predict_yield, name='predict_yield'),
    path('logout/', views.admin_logout, name='admin_logout'),
]
