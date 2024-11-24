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
        errors = {}

        # Validate User Data
        errors.update(User.objects.basic_validator(request.POST))

        # Validate Freelancer-specific Data
        if user_type == 'freelancer':
            errors.update(Freelancer.objects.basic_validator(request.POST))

        # Validate Address
        address_id = request.POST.get('address')
        address = Address.objects.filter(address_id=address_id).first()
        if not address:
            messages.error(request, "Invalid address selected. Please try again.", extra_tags='register')
            return redirect('/')

        if errors:
            for error in errors.values():
                messages.error(request, error, extra_tags='register')
            return redirect('/')

        # Process Registration
        if user_type == 'user':
            address = Address.objects.get(address_id=request.POST.get('address'))
            print("Address Object (User):", address)  # Debugging log

            # Prepare the data for adding a user
            user_data = {
                'fname': request.POST.get('fname'),
                'lname': request.POST.get('lname'),
                'email': request.POST.get('email'),
                'phone_number': request.POST.get('phone_number'),
                'password': request.POST.get('password'),
                'address': address,  # Pass the Address instance directly
            }

            User.objects.add_user(user_data)
            messages.success(request, "User registered successfully! Please log in.")
            return redirect('/login')
        elif user_type == 'freelancer':
            address = Address.objects.get(address_id=request.POST.get('address'))
            print("Address Object (Freelancer):", address)  # Debugging log

            # Fetch the Profession instance
            profession_id = request.POST.get('profession')
            profession = Profession.objects.get(proid=profession_id)

            # Prepare the data for creating a freelancer
            freelancer_data = {
                'fname': request.POST.get('fname'),
                'lname': request.POST.get('lname'),
                'email': request.POST.get('email'),
                'phone_number': request.POST.get('phone_number'),
                'password': request.POST.get('password'),
                'address': address,  # Pass the Address instance directly
                'profession': profession,  # Pass the Profession instance directly
                'profile_picture': request.FILES.get('profile_picture'),
            }

            # Create freelancer
            freelancer = Freelancer.objects.create_freelancer(freelancer_data)

            # Check if there are errors in the freelancer creation
            if isinstance(freelancer, dict):  # Errors
                print("Freelancer creation errors:", freelancer)  # Debugging log
                for error in freelancer.values():
                    messages.error(request, error, extra_tags='register')
                return redirect('/')

            print("Freelancer Object:", freelancer)

            # Save profile picture
            profile_picture = request.FILES.get('profile_picture')
            if profile_picture:
                freelancer.profile_picture = profile_picture
                freelancer.save()

            messages.success(request, "Freelancer registered successfully! Please log in.")
            return redirect('/login')
    else:
        context = {
            'professions': Profession.get_all_professions(),
            'addresses': Address.get_all_addresses()
        }
        return render(request, 'index.html', context)





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
