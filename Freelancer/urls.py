from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

<<<<<<< Updated upstream
from django.urls import path
from . import views
=======
>>>>>>> Stashed changes

urlpatterns = [
<<<<<<< Updated upstream
    path('', views.index, name='freelancer_dashboard'),
    path('fetch/', views.fetch_freelancers, name='fetch-freelancers'),
    path('profile/<int:freelancer_id>/', views.viewfreelancer, name='profile'),
    path('edit_profile/<int:freelancer_id>/', views.update_freelancer_profile, name='edit-freelancer-profile'),
<<<<<<< Updated upstream
    path('post/', views.freelancer_post, name='freelancer_post'),
=======
    path('', views.index, name='freelancer_dashboard'),  # Dashboard for freelancers
    path('fetch/', views.fetch_freelancers, name='fetch-freelancers'),  # Fetch freelancers
    path('profile/<int:freelancer_id>/', views.viewfreelancer, name='profile'),  # View freelancer profile
    path('edit_profile/<int:freelancer_id>/', views.update_freelancer_profile, name='edit-freelancer-profile'),  # Edit freelancer profile
    path('viewfreelancer/<int:freelancer_id>/', views.viewfreelancer, name='viewfreelancer'),  # View freelancer profile with comments
    path('post/', views.freelancer_post, name='freelancer_post'),  # Freelancer post creation and comment handling
>>>>>>> Stashed changes
=======
    # path('post/', views.freelancer_post, name='freelancer_post'),
    path('viewfreelancer/<int:freelancer_id>/', views.viewfreelancer, name='viewfreelancer'),
>>>>>>> Stashed changes
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
