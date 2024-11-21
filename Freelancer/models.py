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
    
    
def add Profession():
    professions = [
        {"proid": 1, "protag": "جنين"},
        {"proid": 2, "protag": "قلقيلية"},
        {"proid": 3, "protag": "تابلس"},
        {"proid": 4, "protag": "طولكرم"},
        {"proid": 5, "protag": "جنين"},
        {"proid": 6, "protag": "سلفيت"},
        {"proid": 7, "protag": "رام الله"},
        {"proid": 8, "protag": "أريحا"},
        {"proid": 9, "protag": "الفدس"},
        {"proid": 10, "protag": "بيت لحم"},
        {"proid": 11, "protag": "الخليل"},
    ]