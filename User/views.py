from django.shortcuts import render, redirect
from User.models import Post, User
from django.contrib import messages

# View to render the user dashboard
def user_dashboard(request):
    user_id = int(request.session['id'])
    user = User.objects.get(id=user_id)
    context = {
        'posts': Post.objects.get_user_posts(user),
    }
    return render(request, 'user_dashboard.html', context)  

# View to render the user profile based on user ID
def user_profile(request):
    return render(request, 'user_profile.html')  

def chat(request, id):
    return render(request, 'chat.html')  

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