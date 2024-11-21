from django.urls import *
from . import views

urlpatterns = [
    path('freelancer', views.index),
]