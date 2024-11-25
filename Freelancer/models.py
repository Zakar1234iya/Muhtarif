from django.db import models
from index.models import Address 
import bcrypt
import threading
from User.models import User

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

    def has_already_commented(self, user, freelancer):
        return Comment.objects.filter(freelancer=freelancer, author=user).exists()


class NotificationManager(models.Manager):
    def add_notification(self, content, freelancer):
        return Notification.objects.create(content=content, freelancer=freelancer)
    def get_notifications(self, freelancer):
        return Notification.objects.filter(freelancer=freelancer)

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
        created_profession = Profession.objects.filter(proid=profession['proid'], protag=profession['protag'])
        if not created_profession.exists():
            Profession.objects.create(proid=profession['proid'], protag=profession['protag'])
            print(f"Created new profession: {profession['protag']}")
        else:
            print(f"Profession already exists: {profession['protag']}")

def delayed_add_pro(delay=5):
    timer = threading.Timer(delay, add_pro)
    timer.start()
    
    
# delayed_add_pro()


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
    profile_picture = models.ImageField(upload_to='freelancer_profiles/', null=True, blank=True)
    tasks = models.PositiveIntegerField(default=0)  # Track the number of tasks
    objects = FreelancerManager()  # Use the custom manager

    def validate_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode(), self.password.encode())

    def rating(self):
        comments = Comment.objects.filter(freelancer=self)
        stars = 0
        ratings = 0
        for comment in comments:
            stars += comment.rating
            ratings += 1
        return stars if stars == 0 else stars / ratings
    
    def get_completed_tasks(self):
        return self.freelancer_tasks.filter(status='completed').count()

# Notification Model
class Notification(models.Model):
    content = models.TextField()
    freelancer = models.ForeignKey(Freelancer, related_name='freelancer_notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = NotificationManager()

# Task Model
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=[('completed', 'Completed'), ('pending', 'Pending')],
    )
    freelancer = models.ForeignKey(Freelancer, related_name='freelancer_tasks', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_tasks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Comment Model
class Comment(models.Model):
    content = models.TextField()
    freelancer = models.ForeignKey(Freelancer, related_name='freelancer_comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    # other fields like timestamp, etc.


    def __str__(self):
        print(f"Freelancer: {self.freelancer.first_name} {self.freelancer.last_name}")  # Debugging
        return f"Comment by {self.creator.username} on {self.freelancer.first_name} {self.freelancer.last_name}"


# Task-related functions
def add_task(title, description, user, freelancer):
    # Adds a new task to the database.
    return Task.objects.create(
        title=title,
        description=description,
        status='pending',
        user=user,
        freelancer=freelancer
    )

def remove_task(task_id):
    # Removes a task with the given task_id.
    task = Task.objects.filter(id=task_id).first()
    if task:
        task.delete()
        return True
    return False

def update_task_status(task, new_status):
    # Updates the status of the given task if the status is valid.
    valid_statuses = [choice[0] for choice in Task._meta.get_field('status').choices]
    if new_status in valid_statuses:
        task.status = new_status
        task.save()
        return True
    return False


def add_comment(content, author, freelancer, rating):
    print(author)
    print(author.fname)
    comment = Comment.objects.create(
        content=content,
        author=author,
        freelancer=freelancer,
        rating=rating
    )
    return comment



def remove_comment(comment_id):
    # Removes a comment with the given comment_id
    comment = Comment.objects.filter(id=comment_id).first()
    if comment:
        comment.delete()
        return True
    return False

def get_comments_for_freelancer(freelancer):
  
    return Comment.objects.filter(freelancer=freelancer).order_by('-created_at')


# ChatSession Model
class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def add_message(self, sender, message_text, current_user_type):
        return ChatMessage.objects.create(session=self, sender=str(sender.id), text=message_text, sender_type=current_user_type)

    def get_messages(self):
        return ChatMessage.objects.filter(session=self)


    def __str__(self):
        return f"Chat between {self.user.fname} and {self.freelancer.fname}"


# ChatMessage Model
class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, related_name="messages", on_delete=models.CASCADE)
    sender = models.TextField()  # sender id
    sender_type = models.TextField()
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:20]}..."


