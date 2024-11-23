from django.db import models
import threading


class Address(models.Model):
    address_id = models.SmallIntegerField(primary_key=True)
    address_name = models.CharField(max_length=50)

    def get_all_addresses():
        return Address.objects.all()
    
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
        created_address = Address.objects.filter(address_id=address['address_id'], address_name=address['address_name'])
        if not created_address.exists():
            Address.objects.create(address_id=address['address_id'], address_name=address['address_name'])
            print(f"Created new address: {address['address_name']}")
        else:
            print(f"Address already exists: {address['address_name']}")
def zak(delay=5):
    timer = threading.Timer(delay, add_address)
    timer.start()

# zak()


# class Freelancer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Add any other fields for freelancer if needed
#     def __str__(self):
#         return self.user.username

# class Chat(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_chats')
#     freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='freelancer_chats')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Chat between {self.user.username} and {self.freelancer.user.username}"

# class Message(models.Model):
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     sent_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Message from {self.sender.username} at {self.sent_at}"
