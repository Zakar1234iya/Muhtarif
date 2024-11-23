from django.urls import *
from . import views

urlpatterns = [
    path('', views.index),
    path('profile', views.profile , name="profile")
]