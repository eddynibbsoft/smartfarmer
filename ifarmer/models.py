from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# models.py

from django.db import models

class Farmer(models.Model):
    full_name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    land_size = models.FloatField()
    crop_type = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=20)


# class InputAllocation(models.Model):
#     farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='input_allocations')
#     water = models.FloatField()
#     fertilizer = models.FloatField()
#     pesticides = models.FloatField()

# class YieldPrediction(models.Model):
#     farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='yield_predictions')
#     predicted_yield = models.FloatField()
