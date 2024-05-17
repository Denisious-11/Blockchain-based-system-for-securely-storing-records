from django.db import models

# Create your models here.
class Requests(models.Model):
    S_id=models.IntegerField(primary_key=True)
    P_address=models.CharField(max_length=255)
    Username=models.CharField(max_length=255)
    Email=models.CharField(max_length=255)
    Password=models.CharField(max_length=255)
    Phone=models.CharField(max_length=255)

class Users(models.Model):
    S_id=models.IntegerField(primary_key=True)
    P_address=models.CharField(max_length=255)
    Username=models.CharField(max_length=255)
    Email=models.CharField(max_length=255)
    Password=models.CharField(max_length=255)
    Phone=models.CharField(max_length=255)
    
class Records(models.Model):
    record_name=models.CharField(max_length=255)
    access=models.CharField(max_length=255)
    date=models.CharField(max_length=255)
    time=models.CharField(max_length=255)
    hash_value=models.CharField(max_length=255)
