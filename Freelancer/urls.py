from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='freelancer_dashboard'),
    path('fetch/', views.fetch_freelancers, name='fetch-freelancers'),
    path('edit_profile/<int:freelancer_id>/', views.edit_freelancer, name='edit_profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



