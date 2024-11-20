from django.db import models
   

class AdminManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        fname = postData.get('fname')
        lname = postData.get('lname')
        email = postData.get('email')
        pasword = postData.get('pasword')
class Admin(models.Model):
    fname = models.CharField(max_length=254)
    lname = models.CharField(max_length=254)
    email = models.EmailField()
    pasword = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    

    