from django.shortcuts import render, redirect
from django.http import HttpResponse ,JsonResponse,Http404
from .models import Freelancer, Address, Profession , User
from Freelancer.models import Freelancer ,Task , get_comments_for_freelancer ,add_comment , Notification, ChatSession
from django.apps import apps
from django.contrib import messages 
from User.models import *
import bcrypt





def index(request):
    freelancer_id = request.session.get('id')
    user_type = request.session.get('type')
    
    # Ensure the logged-in user is of the correct type (freelancer)
    if not freelancer_id or user_type != 'freelancer':
        # Redirect to a general page if the freelancer is not logged in or trying to access the wrong page
        return redirect('/')
    
    # Retrieve the freelancer object by ID
    freelancer = Freelancer.objects.get(id=freelancer_id)
    posts = Post.objects.all()
    notifications = Notification.objects.get_notifications(freelancer)
    context = {
        'freelancer': freelancer,
        'posts': posts,
        'notifications': notifications,
    }
    
    # Render the freelancer dashboard template with the context data
    return render(request, 'dashbord.html', context)


def update_freelancer_profile(request):
    # Fetch the freelancer object
    freelancer_id = int(request.POST['freelancer_id'])
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
                address = Address.objects.filter(address_id=address_id).first()
                if address:
                    freelancer.address = address

            if profession_id:
                profession = Profession.objects.filter(proid=profession_id).first()
                if profession:
                    freelancer.profession = profession

            if new_password:
                hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                freelancer.password = hashed_password
            freelancer.email = email
            freelancer.save()
            print("Profile update successful.")
            messages.success(request, 'تم تحديث الملف الشخصي بنجاح!')
            return redirect('freelancer_dashboard')

        print("Profile update failed with errors.")
        return redirect('freelancer-profile', freelancer_id=freelancer_id)

    return redirect('freelancer-profile', freelancer_id=freelancer_id)


def freelancer_list(request):
    # Check if the user is logged in and is of type 'user'
    user_id = request.session.get('id')
    user_type = request.session.get('type')
    
    if not user_id or user_type != 'user':
        messages.error(request, 'You must be logged in as a user to view this page.')
        return redirect('/')

    # Proceed with the rest of the function if the user is authenticated and of type 'user'
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
    
    context = {
        'freelancer': freelancer,
        'addresses': Address.objects.all(),
        'professions': Profession.objects.all(),
    }
    return render(request, 'freelancer_profile.html', context)



def get_completed_tasks(freelancer):
    return Task.objects.filter(freelancer=freelancer, status='completed').count()


def clear_notifications(request):
    freelancer = Freelancer.objects.get(id=int(request.session['id']))
    notifications = Notification.objects.filter(freelancer=freelancer)
    for notification in notifications:
        notification.delete()
    return redirect('freelancer_dashboard')

def viewfreelancer(request, freelancer_id):
    user_id = request.session.get('id')
    user_type = request.session.get('type')
    
    # Ensure the logged-in user is of the correct type (user)
    if not user_id or user_type != 'user':
        messages.error(request, 'You must be logged in as a user to view this page.')
        return redirect('/')

    # Get the freelancer or show an error if not found
    freelancer = Freelancer.objects.filter(id=freelancer_id).first()
    if not freelancer:
        messages.error(request, 'Freelancer not found.')
        return redirect('/')

    # Get completed tasks count using the helper function
    completed_tasks = freelancer.get_completed_tasks()
    user = User.objects.get(id=int(user_id))
    comments = get_comments_for_freelancer(freelancer)
    existing_comment = Freelancer.objects.has_already_commented(user, freelancer)

    # Context for the template
    context = {
        'freelancer': freelancer,
        'completed_tasks': completed_tasks,
        'comments': comments,
        'has_rated_before': existing_comment
    }
    return render(request, 'freelancer_user.html', context)


def view_chats(request):
    current_user_type = request.session['type']
    if current_user_type == 'user':
        user = User.objects.get(id=int(request.session['id']))
        chats = ChatSession.objects.filter(user=user)
    else:
        user = Freelancer.objects.get(id=int(request.session['id']))
        chats = ChatSession.objects.filter(freelancer=user)
    context = {
        'chats': chats,
        'current_chat': None if not request.session.get('current_chat_id') else ChatSession.objects.get(id=int(request.session['current_chat_id'])),
        'current_user_type': request.session['type'],
        'current_user_id': str(request.session['id'])
    }
    return render(request, 'chats.html', context)

def set_current_chat(request, chat_id):
    request.session['current_chat_id'] = str(chat_id)
    return redirect('chats')

def submit_comment(request):
    user_id = int(request.session.get('id'))
    if not 'id' in request.session:
        messages.error(request, "You must be logged in to comment.")
        return redirect('/login/')
    freelancer_id = int(request.POST['freelancer_id'])
    user = User.objects.get(id=user_id)  # Fetch the logged-in user
    freelancer = Freelancer.objects.get(id=freelancer_id)  # Fetch the freelancer to comment on
    existing_comment = Freelancer.objects.has_already_commented(user, freelancer)
    if existing_comment:
        messages.error(request, "You may not make another rating as you have already rated this freelancer.")
        return redirect('viewfreelancer', freelancer_id=freelancer_id)
    rating = int(request.POST['rating'])
    if request.method == 'POST':
        comment_content = request.POST.get('comment_content')
        if comment_content:
            comment = add_comment(comment_content, user, freelancer, rating)
            notification_content = f'قام {user.fname} {user.lname} بتقييمك {rating}/5'
            Notification.objects.add_notification(notification_content, freelancer)
            if comment:
                messages.success(request, 'Your comment has been posted successfully.')
            else:
                messages.error(request, 'There was an error saving your comment.')
        else:
            messages.error(request, 'Comment content cannot be empty.')
    
    return redirect('viewfreelancer', freelancer_id=freelancer_id)


def add_comment_to_post(request):
    post = Post.objects.get(id=int(request.POST['post_id']))
    user = Freelancer.objects.get(id=int(request.session['id']))
    Comment.objects.create_comment({'content': request.POST['content'], 'creator': user, 'post': post })
    return redirect('freelancer_dashboard')






# def fetch_freelancers(request):
#     profession_id = request.GET.get('profession_id')

#     # Check for valid profession_id
#     if not profession_id or not profession_id.isdigit():
#         return JsonResponse({'error': 'Invalid profession_id'}, status=400)

#     # Fetch freelancers (ensure no redirect is happening)
#     try:
#         profession = Profession.objects.filter(proid=profession_id).first()
#         if not profession:
#             return JsonResponse({'freelancers': []})

#         freelancers = Freelancer.objects.filter(profession=profession)
#         freelancers_data = [
#             {
#                 'id': freelancer.id,
#                 'fname': freelancer.fname,
#                 'lname': freelancer.lname,
#                 'email': freelancer.email,
#                 'photo': freelancer.photo.url if freelancer.photo else None,
#             }
#             for freelancer in freelancers
#         ]
#         return JsonResponse({'freelancers': freelancers_data})
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)


# def freelancer_post(request):
#     freelancer_id = request.session.get('id')
#     user_type = request.session.get('type')
    
#     # Ensure the logged-in user is of the correct type (freelancer)
#     if not freelancer_id or user_type != 'freelancer':
#         # Redirect to a general page if the freelancer is not logged in or trying to access the wrong page
#         return redirect('/')
    
#     # Retrieve the freelancer object by ID
#     freelancer = Freelancer.objects.get(id=freelancer_id)
    
#     # Fetch posts created by users
#     posts = Post.objects.all().order_by('-created_at')
    
#     if request.method == 'POST':
#         content = request.POST.get('comment_content')
#         post_id = request.POST.get('post_id')
#         post = Post.objects.get(id=post_id)
        
#         # Create a new comment
#         comment = Comment(content=content, creator=freelancer, post=post)
#         comment.save()
#         messages.success(request, 'تم إضافة التعليق بنجاح!')
#         return redirect('freelancer_post')
    
#     context = {
#         'freelancer': freelancer,
#         'posts': posts
#     }
    
#     # Render the post template with the context data
#     return render(request, 'post.html', context)
