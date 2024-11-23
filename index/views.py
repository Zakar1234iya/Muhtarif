from django.shortcuts import render, redirect
from django.http import HttpResponse
from User.models import User  # Import User model
from Freelancer.models import Freelancer, Profession  
from django.contrib import messages
from django.http import JsonResponse
from .models import *
import bcrypt
from .models import Address

def index(request):
    context = {
        'professions': Profession.get_all_professions(),
        'addresses': Address.get_all_addresses()
    }
    return render(request, 'index.html', context)



def service(request):
    return render(request , 'Services.html')

def register(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')  
        
        errors = User.objects.basic_validator(request.POST)
        if errors:
            for error in errors.values():
                messages.error(request, error, extra_tags='register')
            return redirect('/')
        if user_type == 'user':
            user = User.objects.add_user(request.POST)
            request.session['id'] = user.id
            request.session['type'] = 'user'
            request.session['fname'] = user.fname
            return redirect('user_dashboard')
        elif user_type == 'freelancer':
            user = Freelancer.objects.create_freelancer(request.POST)
            request.session['id'] = user.id
            request.session['type'] = 'freelancer'
            request.session['fname'] = user.fname
            return redirect('freelancer_dashboard')
    return render('/')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email).first()
        freelancer = Freelancer.objects.filter(email=email).first()
        
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            print('ul')
            request.session['id'] = user.id
            request.session['type'] = 'user'
            request.session['fname'] = user.fname
            return redirect('user_dashboard')
        elif freelancer and bcrypt.checkpw(password.encode(), freelancer.password.encode()):
            print('fl')
            request.session['id'] = freelancer.id
            request.session['type'] = 'freelancer'
            request.session['fname'] = freelancer.fname
            return redirect('freelancer_dashboard')
        else:
            print('error')
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
