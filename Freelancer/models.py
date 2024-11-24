from django.db import models
from index.models import Address
import bcrypt
import threading


class FreelancerManager(models.Manager):

    def basic_validator(self, postdata):
        errors = {}

        fname = postdata.get('fname')
        lname = postdata.get('lname')
        email = postdata.get('email')
        phone_number = postdata.get('phone_number')
        password = postdata.get('password')
        address = postdata.get('address')
        profession = postdata.get('profession')

        # Validation checks (same as User model)
        if not fname or len(fname) < 3:
            errors["fname"] = "First name must be at least 3 characters long."
        if not lname or len(lname) < 3:
            errors["lname"] = "Last name must be at least 3 characters long."
        if not email:
            errors["email"] = "Email is required."
        elif Freelancer.objects.filter(email=email).exists():
            errors["email"] = "Email already exists."
        if not phone_number or len(phone_number) != 10 or not phone_number.isdigit():
            errors["phone_number"] = "Phone number must be 10 digits long."
        if not password or len(password) < 8:
            errors["password"] = "Password must be at least 8 characters long."
        if not address:
            errors["address"] = "Address is required."
        if not profession:
            errors["profession"] = "Profession is required."

        return errors

    def create_freelancer(self, data):
        # Step 1: Validate the incoming data
        errors = self.basic_validator(data)
        if errors:
            return errors  # Return validation errors if they exist

        # Step 2: Hash the password securely using bcrypt
        hashed_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()

        # Step 3: Create the Freelancer object with validated data
        freelancer = self.create(
            fname=data['fname'],
            lname=data['lname'],
            email=data['email'],
            phone_number=data['phone_number'],
            password=hashed_password,
            address=data['address'],
            profession=data['profession'],
            profile_picture=data.get('profile_picture')  # If profile picture is optional
        )

        return freelancer  # Return the newly created Freelancer object



    def edit_freelancer(self, freelancer_id, postdata):
        freelancer = self.get(id=freelancer_id)

        # Validate data and capture errors
        errors = self.basic_validator(postdata)
        if errors:
            return errors  # Return errors if validation fails

        # Update fields
        freelancer.fname = postdata['fname']
        freelancer.lname = postdata['lname']
        freelancer.email = postdata['email']
        freelancer.phone_number = postdata['phone_number']
        freelancer.address = Address.objects.get(id=postdata['address_id'])
        freelancer.profession = Profession.objects.get(proid=postdata['profession_id'])
        freelancer.save()
        return freelancer

class Profession(models.Model):
    proid = models.SmallIntegerField(primary_key=True)  # Set as primary key
    protag = models.CharField(max_length=50)

    
    def get_all_professions():
        return Profession.objects.all()


def add_pro():
    professions = [
        {"proid": 1, "protag": "فني ستلايت"},
        {"proid": 2, "protag": "فني صيانة أجهزة منزلية"},
        {"proid": 3, "protag": "فني سباكة"},
        {"proid": 4, "protag": "فني كهرباء"},
        {"proid": 5, "protag": "فني تكييف وتبريد"},
        {"proid": 6, "protag": "فني دهان"},
        {"proid": 7, "protag": "فني كاميرات"},
        {"proid": 8, "protag": "فني نجارة"},
        {"proid": 9, "protag": "فني بلاط"},
        {"proid": 10, "protag": "فني زجاج والمنوم"},
        {"proid": 11, "protag": "فني حدادة"},
        {"proid": 12, "protag": "فني جبصين"},
    ]

    for profession in professions:
        obj, created = Profession.objects.get_or_create(
            proid=profession['proid'],
            defaults={'protag': profession['protag']}
        )
        if created:
            print(f"Added Profession: {profession['protag']}")
        else:
            print(f"Profession with proid {profession['proid']} already exists.")

def delayed_add_pro(delay=60):
    timer = threading.Timer(delay, add_pro)
    timer.start()

class Freelancer(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    password = models.CharField(max_length=254)  # Stores bcrypt-hashed password
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)  
    rating_total = models.PositiveIntegerField(default=0)
    rating_count = models.PositiveIntegerField(default=0)
    profile_picture = models.ImageField(upload_to='freelancer_profiles/', null=True, blank=True)
    objects = FreelancerManager()
    def validate_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode(), self.password.encode())

    def average_rating(self):
        if self.rating_count == 0:
            return 0
        return self.rating_total / self.rating_count

# Call the delayed_add_pro function
# delayed_add_pro()
