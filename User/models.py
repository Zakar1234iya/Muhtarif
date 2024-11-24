from django.db import models
import bcrypt
import re
from index.models import Address  # Address is defined in the index app

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')




class CommentManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['content']) < 1:
            errors["content"] = "You cannot publish an empty comment."
        return errors

    def delete_comment(self, comment_id):
        comment = Comment.objects.filter(id=comment_id).first()
        if comment:
            comment.delete()
        else:
            return "Comment does not exist."

    def update_comment(self, comment, new_content):
        comment.content = new_content
        comment.save()

    def create_comment(self, data):
        return self.create(content=data['content'], creator=data['creator'], post=data['post'])

    def get_post_comments(self, post):
        return self.filter(post=post).order_by('-created_at')

    def get_all_comments(self):
        return self.all()

class PostsManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['content']) < 1:
            errors["content"] = "You cannot publish an empty post."
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


# Manager for User
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
        return self.create(
            fname=data['fname'],
            lname=data['lname'],
            email=data['email'],
            phone_number=data['phone_number'],
            password=hashed_password,
            address=data['address'],
            profile_picture=data.get('profile_picture')
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


# User Model
class User(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    password = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='user_profiles/', null=True, blank=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.fname} {self.lname} ({self.email})"



# Post Model
class Post(models.Model):
    content = models.TextField()
    creator = models.ForeignKey(User, related_name="all_posts", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostsManager()

    def __str__(self):
        return f"Post by {self.creator.fname}: {self.content[:20]}..."

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()

    def __str__(self):
        return f"Comment by {self.creator.fname}: {self.content[:20]}..."

# ChatSession Model
class ChatSession(models.Model):
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    freelancer = models.ForeignKey('Freelancer.Freelancer', on_delete=models.CASCADE)
    started = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def start_chat(self, user):
        if user != self.user:
            raise PermissionError("Only the user can start the chat.")
        self.started = True
        self.save()

    def add_message(self, sender, message_text):
        if not self.started:
            raise PermissionError("Chat has not been started yet.")
        if sender not in ['user', 'freelancer']:
            raise ValueError("Sender must be either 'user' or 'freelancer'.")
        message = ChatMessage(session=self, sender=sender, text=message_text)
        message.save()

    def get_messages(self):
        return self.messages.all()


    def __str__(self):
        return f"Chat between {self.user.fname} and {self.freelancer.fname}"


# ChatMessage Model
class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, related_name="messages", on_delete=models.CASCADE)
    sender = models.CharField(max_length=10)  # 'user' or 'freelancer'
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:20]}..."


