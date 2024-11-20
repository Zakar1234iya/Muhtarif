from django.db import models

class Address(models.Model):
    address_id = models.SmallIntegerField()
    address_name = models.CharField(max_length=50)


def add_address():
    Address