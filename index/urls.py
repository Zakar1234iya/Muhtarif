from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('service', views.service),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('About_us/', views.About_us, name='About_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('fqa/', views.fqa, name='fqa'),
    path('logout', views.logout, name='logout'),
    path('freelancers/', include('Freelancer.urls')),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
