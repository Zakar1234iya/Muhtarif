from django.db import models
from address.models import Address

class Profession(models.Model):
    proid = models.SmallIntegerField()
    protag = models.CharField(max_length=50)

class Freelancer(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.SmallIntegerField(max_length=10)
    password = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(Address)
    profession = models.ForeignKey(Profession)
    
    
def add_pro():
    Profession = [
        {"proid": 1, "protag": "فني ستلايت"},
        {"proid": 2, "protag": "فني صيانة أجهزة منزلية"},
        {"proid": 3, "protag": "فني سباكة"},
        {"proid": 4, "protag": "فني كهرباء"},
        {"proid": 5, "protag": "فني تكييف وتبريد"},
        {"proid": 6, "protag": "فني دهان"},
        {"proid": 7, "protag": "فني كاميرات"},
        {"proid": 8, "protag": "فني نجارة"},
        {"proid": 9, "protag": "فني بلاط "},
        {"proid": 10, "protag": "فني نجارة"},
        {"proid": 11, "protag": "فني بلاط"},
        {"proid": 12, "protag": "فني جبصين"},
  
    ]