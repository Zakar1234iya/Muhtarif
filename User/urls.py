from django.urls import *
from . import views

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('profile', views.user_profile , name="user_profile"),
    path('chat', views.chat , name="chat"),
    path('create_post', views.create_post, name='create_post'),
]