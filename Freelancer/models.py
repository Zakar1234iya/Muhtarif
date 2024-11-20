from django.db import models

class Freelancer(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.SmallIntegerField(max_length=10)
    password = models.CharField(max_length=254)
    
    