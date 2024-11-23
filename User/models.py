
from django.db import models
import re
import bcrypt
from index.models import Address  #  Address is defined in the index app

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class PostsManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['content']) < 1:
            errors["content"] = "You cannot publish an empty post."
            return errors
        return errors
    def delete_post(self, post_id):
        post = Post.objects.get(id=post_id)
        post.delete()
    def update_post(self, post, new_content):
        post.content = new_content
        post.save()
    def create_post(self, data):
        return Post.objects.create(content=data['content'], creator=data['creator'])
    def get_user_posts(self, user):
        return Post.objects.filter(creator=user).order_by('-created_at')
    def get_all_posts(self):
        return Post.objects.all()

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['fname']) < 3:
            errors["fname"] = "First name should be at least 3 characters."
        if len(postData['lname']) < 3:
            errors["lname"] = "Last name should be at least 3 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters."
        if User.objects.filter(email=postData['email']).exists():
            errors["email"] = "Email already exists."
        if not postData['phone_number'].isdigit() or len(postData['phone_number']) != 10:
            errors['phone_number'] = "Phone number must be exactly 10 digits."
        if not postData['user_type']:
            errors['user_type'] = "User type is required"
        return errors

    def add_user(self, data):
        hashed_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
        address = Address.objects.get(address_id=int(data['address']))
        print('add_user_reached models')
        return self.create(
            fname=data['fname'],
            lname=data['lname'],
            email=data['email'],
            phone_number=data['phone_number'],
            password=hashed_password,
            address=address
        )

    def edit_user(self, user_id, data):
        user = self.get(id=user_id)
        user.fname = data['fname']
        user.lname = data['lname']
        user.email = data['email']
        user.phone_number = data['phone_number']
        user.address = Address.objects.get(id=data['address_id'])  # Update address
        user.save()
        return user

class User(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    password = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    objects = UserManager()

class Post(models.Model):
    content = models.TextField()
    creator = models.ForeignKey(User, related_name = "all_posts", on_delete = models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostsManager()

    # return user info 
    # def __str__(self):
    #     return f"{self.fname} {self.lname} - {self.email}"

