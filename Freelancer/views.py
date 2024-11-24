from django.shortcuts import render, redirect
from django.http import HttpResponse ,JsonResponse,Http404
from .models import Freelancer, Address, Profession
from Freelancer.models import Freelancer 
from django.apps import apps
from django.contrib import messages
from User.models import User  
import bcrypt
from User.models import Post, Comment



def index(request):
    freelancer_id = request.session.get('id')
    user_type = request.session.get('type')
    
    # Ensure the logged-in user is of the correct type (freelancer)
    if not freelancer_id or user_type != 'freelancer':
        # Redirect to a general page if the freelancer is not logged in or trying to access the wrong page
        return redirect('/')
    
    # Retrieve the freelancer object by ID
    freelancer = Freelancer.objects.get(id=freelancer_id)
    context = {
        'freelancer': freelancer
    }
    
    # Render the freelancer dashboard template with the context data
    return render(request, 'dashbord.html', context)


def update_freelancer_profile(request, freelancer_id):
    # Fetch the freelancer object
    freelancer = Freelancer.objects.filter(id=freelancer_id).first()
    if not freelancer:
        messages.error(request, 'Freelancer not found.')
        return redirect('edit-freelancer-profile', freelancer_id=freelancer_id)

    if request.method == 'POST':
        errors = {}

        # Get form data
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        email = request.POST.get('email')

        # Manually check if the old password matches
        if not bcrypt.checkpw(old_password.encode(), freelancer.password.encode()):
            errors['old_password'] = 'كلمة المرور القديمة غير صحيحة.'

        # Check if new passwords match
        if new_password and new_password != confirm_new_password:
            errors['new_password'] = 'كلمات المرور الجديدة غير متطابقة.'

        # Check if email already exists (allow current email)
        if email != freelancer.email and Freelancer.objects.filter(email=email).exists():
            errors['email'] = 'البريد الإلكتروني موجود بالفعل.'

        # If no errors, update the freelancer profile
        if not errors:
            freelancer.fname = request.POST.get('fname')
            freelancer.lname = request.POST.get('lname')
            freelancer.phone_number = request.POST.get('phone_number')
            address_id = request.POST.get('address_id')
            profession_id = request.POST.get('profession_id')

            if address_id:
                address = Address.objects.filter(id=address_id).first()
                if address:
                    freelancer.address = address

            if profession_id:
                profession = Profession.objects.filter(id=profession_id).first()
                if profession:
                    freelancer.profession = profession

            if new_password:
                hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                freelancer.password = hashed_password
            freelancer.email = email
            freelancer.save()
            print("Profile update successful.")
            messages.success(request, 'تم تحديث الملف الشخصي بنجاح!')
            return redirect('freelancer_dashboard', freelancer_id=freelancer_id)

        print("Profile update failed with errors.")
        return render(request, 'freelancer_profile.html', {
            'freelancer': freelancer,
            'addresses': Address.objects.all(),
            'professions': Profession.objects.all(),
            'errors': errors,})

    return render(request, 'freelancer_profile.html', 
                  {
        'freelancer': freelancer,
        'addresses': Address.objects.all(),
        'professions': Profession.objects.all(),
    })



def freelancer_list(request):
    profession_id = request.GET.get('profession_id')
    if not profession_id:
        context = {
            'error': 'No profession ID provided',
            'freelancers': [],
        }
        return render(request, 'freelancer_list.html', context)

    if not profession_id.isdigit():
        context = {
            'error': 'Invalid profession ID',
            'freelancers': [],
        }
        return render(request, 'freelancer_list.html', context)

    freelancers = Freelancer.objects.filter(profession__proid=int(profession_id))
    context = {
        'freelancers': freelancers,
    }
    return render(request, 'freelancer_list.html', context)



def freelancer_profile(request, freelancer_id):
    freelancer = Freelancer.objects.filter(id=freelancer_id).first()
    if not freelancer:
        raise Http404("Freelancer not found")

    return render(request, 'freelancer_profile.html', {'freelancer': freelancer})


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





def freelancer_post(request):
    freelancer_email = request.session.get('email')
    user_type = request.session.get('type')
    
    # Ensure the logged-in user is of the correct type (freelancer)
    if not freelancer_email or user_type != 'freelancer':
        # Redirect to a general page if the user is not logged in or trying to access the wrong page
        return redirect('/')
    
    # Retrieve the freelancer object by email
    freelancer = Freelancer.objects.filter(email=freelancer_email).first()
    if not freelancer:
        messages.error(request, 'Freelancer not found.')
        return redirect('/')

    # Retrieve the User instance
    user = User.objects.filter(email=freelancer_email).first()
    if not user:
        messages.error(request, 'User not found.')
        return redirect('/')

    # Fetch posts created by users
    posts = Post.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        content = request.POST.get('comment_content')
        post_id = request.POST.get('post_id')
        post = Post.objects.filter(id=post_id).first()
        if post:
            # Create a new comment
            comment = Comment.objects.create(content=content, creator=user, post=post)
            messages.success(request, 'تم إضافة التعليق بنجاح!')
        else:
            messages.error(request, 'Post not found.')
        return redirect('freelancer_post')
    
    context = {
        'freelancer': freelancer,
        'posts': posts
    }
    
    # Render the post template with the context data
    return render(request, 'Freelancer/post.html', context)
