from django.db import models
from index.models import Address
from django.core.exceptions import ValidationError
import bcrypt


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

    def create_freelancer(self, postdata):
        # Validate data and capture errors
        errors = self.basic_validator(postdata)
        if errors:
            return errors  # Return errors if validation fails

        # Hash the password
        hashed_password = bcrypt.hashpw(postdata['password'].encode(), bcrypt.gensalt()).decode()

        # Retrieve Address and Profession objects
        address = Address.objects.get(id=postdata['address_id'])
        profession = Profession.objects.get(proid=postdata['profession_id'])

        # Create Freelancer instance and save
        freelancer = self.create(
            fname=postdata['fname'],
            lname=postdata['lname'],
            email=postdata['email'],
            phone_number=postdata['phone_number'],
            password=hashed_password,
            address=address,
            profession=profession
        )
        return freelancer

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
    proid = models.SmallIntegerField(unique=True)  # Unique identifier for profession
    protag = models.CharField(max_length=50)  # Profession name or tag

    def __str__(self):
        return self.protag

    @staticmethod
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
            {"proid": 9, "protag": "فني بلاط "},
            {"proid": 10, "protag": "فني زجاج والمنوم"},
            {"proid": 11, "protag": "فني حدادة "},
            {"proid": 12, "protag": "فني جبصين"},
        ]
        
        for profession in professions:
            # Check if the profession already exists by proid
            if not Profession.objects.filter(proid=profession['proid']).exists():
                # If not, create a new Profession object
                Profession.objects.create(proid=profession['proid'], protag=profession['protag'])
                print(f"Added Profession: {profession['protag']}")
            else:
                print(f"Profession with proid {profession['proid']} already exists.")


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
    objects = FreelancerManager()
    def validate_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode(), self.password.encode())
