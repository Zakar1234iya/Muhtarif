from django.shortcuts import render, redirect
from django.http import HttpResponse
from User.models import User  # Import User model
from Freelancer.models import Freelancer, Profession  # Import Freelancer and Profession models
from django.contrib import messages
from django.http import JsonResponse
from .models import *
import bcrypt


def index(request):
    return render(request , 'index.html')

def service(request):
    return render(request , 'Services.html')

def register(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')  # Use .get() to avoid MultiValueDictKeyError
        
        if not user_type:  # Handle the case where user_type is not sent
            messages.error(request, "User type is required.", extra_tags='register')
            return redirect('/')

        if user_type == 'user':
            errors = User.objects.basic_validator(request.POST)
            if errors:
                for error in errors.values():
                    messages.error(request, error, extra_tags='register')
                return redirect('/')
            User.objects.add_user(request.POST)
        elif user_type == 'freelancer':
            Freelancer.objects.add_freelancer(request.POST)
        
        messages.success(request, "Registration successful! Please log in.", extra_tags='register')
        return redirect('/')
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email).first()
        freelancer = Freelancer.objects.filter(email=email).first()

        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['id'] = user.id
            request.session['type'] = 'user'
            request.session['fname'] = user.fname
            return redirect('/')
        elif freelancer and bcrypt.checkpw(password.encode(), freelancer.password.encode()):
            request.session['id'] = freelancer.id
            request.session['type'] = 'freelancer'
            request.session['fname'] = freelancer.fname
            return redirect('/')
        else:
            messages.error(request, "Invalid email or password", extra_tags='login')
            return redirect('/')

    return render(request, 'index.html')

def logout(request):
    request.session.flush()
    return redirect('/')


def get_freelancers(request):
    profession_id = request.GET.get('profession_id')
    freelancers = Freelancer.objects.filter(profession__id=profession_id)
    freelancers_data = [
        {
            'fname': freelancer.fname,
            'lname': freelancer.lname,
            'email': freelancer.email,
            'phone_number': freelancer.phone_number,
        }
        for freelancer in freelancers
    ]
    return JsonResponse(freelancers_data, safe=False)



def About_us(request):
    return render(request , 'About_us.html')

def contact_us(request):
    return render(request , 'contact_us.html')

def fqa(request):
    return render(request , 'fqa.html')
