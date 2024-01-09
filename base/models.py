from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission

from django import forms


class Image(models.Model):
    image = models.ImageField(upload_to='images')

    # def __str__(self):
    #     return self.title

    class Meta:
        db_table = "food_scan"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    abdomen = models.FloatField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bmi = models.FloatField(blank=True, null=True)

class Nutrients(models.Model):
    food = models.CharField(max_length=100)
    desc = models.TextField()
    energy = models.FloatField()
    carbohydrates = models.FloatField()
    protien = models.FloatField()
    fat = models.FloatField()
    sugar = models.FloatField()
    health_score = models.FloatField()