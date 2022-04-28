
from django.db import models
from django import forms  

# Create your models here.
from django.contrib.auth.models import AbstractUser


     


class CustomUser(AbstractUser):   
    Date_Of_Birth =models.DateTimeField(blank=True,null=True)
    country=models.CharField(max_length=20,blank=True,null=True)
    Profession=models.CharField(max_length=20,blank=True,null=True)
    gender = models.CharField(max_length=20)
    image = models.ImageField(upload_to ='profile/',blank=True,null=True)
    
class Photo(models.Model):
    file = models.ImageField()
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'
        
         
    



