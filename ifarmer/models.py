from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# models.py

from django.db import models

class Farmer(models.Model):
    full_name = models.CharField(max_length=100)
    region = models.CharField(max_length=10)
    land_size = models.IntegerField()
    crop_type = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=100)
    rainfall = models.CharField(max_length=100)
    temperature = models.CharField(max_length=100)
    address = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)

class Dataset(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='datasets/')
    

    def __str__(self):
        return self.name

class InputAllocation(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    seeds = models.IntegerField()
    fertilizer = models.IntegerField()
    pesticides = models.IntegerField()

class YieldPrediction(models.Model):
    farmer = models.OneToOneField(Farmer, on_delete=models.CASCADE)
    predicted_yield = models.FloatField()

