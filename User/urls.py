from django.urls import *
from . import views

urlpatterns = [
    path('', views.user_dashboard),
    path('profile', views.chat , name="user_profile"),
    path('chat', views.user_profile , name="chat")
]