from django.db import models

class Address(models.Model):
    address_id = models.SmallIntegerField()
    address_name = models.CharField(max_length=50)


def add_address():
    addresses = [
        {"address_id": 1, "address_name": "جنين"},
        {"address_id": 2, "address_name": "طوباس"},
        {"address_id": 3, "address_name": "تابلس"},
        {"address_id": 4, "address_name": "طولكرم"},
        {"address_id": 5, "address_name": "قلقيلية"},
        {"address_id": 6, "address_name": "سلفيت"},
        {"address_id": 7, "address_name": "رام الله"},
        {"address_id": 8, "address_name": "أريحا"},
        {"address_id": 9, "address_name": "الفدس"},
        {"address_id": 10, "address_name": "بيت لحم"},
        {"address_id": 11, "address_name": "الخليل"},
    ]
    
    for address in addresses:
        Address.objects.create(**address)



