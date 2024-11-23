from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Freelancer, Address, Profession

def index(request):
    return render(request , 'dashbord.html')
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
