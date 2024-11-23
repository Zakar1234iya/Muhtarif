from django.urls import *
from . import views

urlpatterns = [
    path('', views.index, name='freelancer_dashboard'),
    # path('profile', views.profile , name="profile")
]