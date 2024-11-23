from django.shortcuts import render

# View to render the user dashboard
def user_dashboard(request):
    return render(request, 'user_dashboard.html')  

# View to render the user profile based on user ID
def user_profile(request, id):
    return render(request, 'user_profile.html')  

def chat(request, id):
    return render(request, 'chat.html')  
