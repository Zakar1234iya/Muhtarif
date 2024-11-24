from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='freelancer_dashboard'),
    path('fetch/', views.fetch_freelancers, name='fetch-freelancers'),
    path('profile/<int:freelancer_id>/', views.freelancer_profile, name='freelancer-profile'),
    path('edit_profile/<int:freelancer_id>/', views.update_freelancer_profile, name='edit-freelancer-profile'),
    path('post/', views.freelancer_post, name='freelancer_post'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


