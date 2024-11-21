from django.shortcuts import render

def index(request):
    return render(request , 'FL_Dashboard.html')