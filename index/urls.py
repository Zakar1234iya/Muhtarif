from django.urls import *
from . import views

urlpatterns = [
    path('', views.index,),
    path('service' , views.service),
]