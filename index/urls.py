from django.urls import *
from . import views

urlpatterns = [
    path('', views.index,),
    path('service' , views.service),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('freelancers', views.get_freelancers, name='get_freelancers'),
    path('About_us/', views.About_us, name='About_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('fqa/', views.fqa, name='fqa'),
    path('logout', views.logout, name='logout'),
]

