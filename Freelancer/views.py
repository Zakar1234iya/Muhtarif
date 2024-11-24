from django.shortcuts import render, redirect
from django.http import HttpResponse ,JsonResponse,Http404
from .models import Freelancer, Address, Profession
from Freelancer.models import Freelancer 
from django.apps import apps
from django.contrib import messages
from User.models import User  

# Other view functions here...


def index(request):
    freelancer_id = request.session.get('id')
    user_type = request.session.get('type')
    
    # Ensure the logged-in user is of the correct type (freelancer)
    if not freelancer_id or user_type != 'freelancer':
        # Redirect to a general page if the freelancer is not logged in or trying to access the wrong page
        return redirect('/')
    
    freelancer = Freelancer.objects.get(id=freelancer_id)  # Retrieve the freelancer object by ID
    context = {
        'freelancer': freelancer
    }
    return render(request, 'dashbord.html', context)

def add_freelancer(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        address_id = request.POST.get('address_id')
        profession_id = request.POST.get('profession_id')

        postdata = {
            'fname': fname,
            'lname': lname,
            'email': email,
            'phone_number': phone_number,
            'password': password,
            'address': address_id,
            'profession': profession_id
        }

        # Create freelancer using the manager method
        errors = Freelancer.objects.create_freelancer(postdata)
        if errors:
            context = {
                'errors': errors,
                'professions': Profession.get_all_professions(),
                'addresses': Address.get_all_addresses()
            }
            return render(request, 'add_freelancer.html', context)

        return redirect('success_page')  # Replace with the actual success page
    else:
        context = {
            'professions': Profession.get_all_professions(),
            'addresses': Address.get_all_addresses()
        }
        return render(request, 'add_freelancer.html', context)



def edit_freelancer(request, freelancer_id):
    freelancers = Freelancer.objects.filter(id=freelancer_id)
    if not freelancers.exists():
        return HttpResponse('Freelancer not found', status=404)
    
    freelancer = freelancers.first()
    
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if not freelancer.validate_password(old_password):
            errors = {'old_password': 'كلمة المرور القديمة غير صحيحة.'}
            context = {
                'errors': errors,
                'freelancer': freelancer,
                'professions': Profession.get_all_professions(),
                'addresses': Address.get_all_addresses()
            }
            return render(request, 'edit_freelancer.html', context)

        if new_password and new_password != confirm_new_password:
            errors = {'new_password': 'كلمة المرور الجديدة غير متطابقة.'}
            context = {
                'errors': errors,
                'freelancer': freelancer,
                'professions': Profession.get_all_professions(),
                'addresses': Address.get_all_addresses()
            }
            return render(request, 'edit_freelancer.html', context)

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address_id = request.POST.get('address_id')
        profession_id = request.POST.get('profession_id')

        postdata = {
            'fname': fname,
            'lname': lname,
            'email': email,
            'phone_number': phone_number,
            'address': address_id,
            'profession': profession_id
        }

        if new_password:
            postdata['password'] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

        # Edit freelancer using the manager method
        errors = Freelancer.objects.edit_freelancer(freelancer_id, postdata)
        if errors:
            context = {
                'errors': errors,
                'freelancer': freelancer,
                'professions': Profession.get_all_professions(),
                'addresses': Address.get_all_addresses()
            }
            return render(request, 'edit_freelancer.html', context)

        return redirect('/')  # Replace with the actual success page
    else:
        context = {
            'freelancer': freelancer,
            'professions': Profession.get_all_professions(),
            'addresses': Address.get_all_addresses()
        }
        return render(request, 'edit_freelancer.html', context)


def freelancer_list(request):
    profession_id = request.GET.get('profession_id')
    if profession_id and profession_id.isdigit():
        freelancers = Freelancer.objects.filter(job_category__proid=int(profession_id))
    else:
        freelancers = Freelancer.objects.all()

    return render(request, 'freelancer/freelancer_list.html', {'freelancers': freelancers})


def freelancer_profile(request, freelancer_id):
    freelancer = Freelancer.objects.filter(id=freelancer_id).first()
    if not freelancer:
        raise Http404("Freelancer not found")

    return render(request, 'freelancer/freelancer_profile.html', {'freelancer': freelancer})


def fetch_freelancers(request):
    profession_id = request.GET.get('profession_id')

    # Check for valid profession_id
    if not profession_id or not profession_id.isdigit():
        return JsonResponse({'error': 'Invalid profession_id'}, status=400)

    # Fetch freelancers (ensure no redirect is happening)
    try:
        profession = Profession.objects.filter(proid=profession_id).first()
        if not profession:
            return JsonResponse({'freelancers': []})

        freelancers = Freelancer.objects.filter(profession=profession)
        freelancers_data = [
            {
                'id': freelancer.id,
                'fname': freelancer.fname,
                'lname': freelancer.lname,
                'email': freelancer.email,
                'photo': freelancer.photo.url if freelancer.photo else None,
            }
            for freelancer in freelancers
        ]
        return JsonResponse({'freelancers': freelancers_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

