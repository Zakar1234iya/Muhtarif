from django.shortcuts import render, redirect
from User.models import Post, User  
from django.contrib import messages
from index.models import Address 
from Freelancer.models import Freelancer, ChatSession, ChatMessage, Notification

# View to render the user dashboard

def user_dashboard(request):
    user_id = request.session.get('id')
    user_type = request.session.get('type')
    
    # Ensure the logged-in user is of the correct type (user)
    if not user_id or user_type != 'user':
        # Redirect to a general page if the user is not logged in or trying to access the wrong page
        return redirect('home')
    
    user = User.objects.get(id=user_id)  # Retrieve the user object by ID
    posts = Post.objects.filter(creator=user)  # Fetch posts related to this user
    posts_refined = []
    for post in posts:
        post_data = {
            'post': post,
        }
        if post.done:
            hired_freelancer = Freelancer.objects.filter(id=post.done_by).first()
            if hired_freelancer:
                post_data['hired_freelancer'] = hired_freelancer
        posts_refined.append(post_data)
    context = {
        'posts': posts_refined,
        'user': user
    }
    return render(request, 'user_dashboard.html', context)



# View to render the user profile page
def user_profile(request, id):
    user = User.objects.filter(id=id).first()  # Retrieve the user by ID

    # If the user does not exist, redirect to login with an error message
    if not user:
        messages.error(request, "المستخدم غير موجود.")
        return redirect('login')

    # Access the address_name from the related Address model
    address_name = user.address.address_name if user.address else None

    context = {
        'user': user,
        'address_name': address_name,  # Pass the address_name to the template
    }

    return render(request, 'user_profile.html', context)



def create_post(request):
    errors = Post.objects.basic_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='create_post')
        return redirect('user_dashboard')
    user_id = int(request.session['id'])
    user = User.objects.get(id=user_id)
    Post.objects.create_post({'content': request.POST['content'], 'creator': user})
    return redirect('user_dashboard')

def delete_post(request, post_id):
    post = Post.objects.filter(id=post_id).first()  
    if post:
        post.delete()
    return redirect('user_dashboard')  


def hire_comment(request):
    freelancer = Freelancer.objects.get(id=int(request.POST['freelancer_id']))
    user_id = int(request.session['id'])
    user = User.objects.get(id=user_id)
    post = Post.objects.get(id=int(request.POST['post_id']))
    post.done = True
    post.done_by = freelancer.id
    post.save()
    freelancer.tasks += 1
    freelancer.save()
    notification_content = f'قام {user.fname} {user.lname} بتوظيفك للقيام بمهمة'
    Notification.objects.add_notification(notification_content, freelancer)
    return redirect('user_dashboard')


def send_chat(request):
    current_user_type = request.session['type']
    if current_user_type == 'user':
        user = User.objects.get(id=int(request.session['id']))
    else:
        user = Freelancer.objects.get(id=int(request.session['id']))
    chat_session = ChatSession.objects.get(id=int(request.POST['chatsession_id']))
    chat_session.add_message(user, request.POST['message'], current_user_type)
    return redirect('chats')


def start_chat(request, freelancer_id):
    user_id = request.session.get('id')
    user_type = request.session.get('type')
    # Check if the logged-in user is a 'user' type
    if user_type != 'user':
        messages.error(request, "فقط المستخدم يمكنه بدء المحادثة.")
        return redirect('user_dashboard')

    # Get the user and freelancer objects
    user = User.objects.get(id=int(user_id))
    freelancer = Freelancer.objects.get(id=freelancer_id)

    # Check if a chat session already exists between the user and freelancer
    chat_session = ChatSession.objects.filter(user=user, freelancer=freelancer).first()

    # If no chat session exists, create a new one
    if not chat_session:
        chat_session = ChatSession.objects.create(user=user, freelancer=freelancer)
        notification_content = f'قام {user.fname} {user.lname} ببدأ محادثة معك'
        Notification.objects.add_notification(notification_content, freelancer)
        

    # Fetch messages for the chat session
    messages = chat_session.get_messages()

    context = {
        'messages': messages,
        'chat_session': chat_session
    }
    request.session['current_chat_id'] = str(chat_session.id)
    return redirect('chats')

