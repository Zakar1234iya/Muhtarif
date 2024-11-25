from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='freelancer_dashboard'),  # Freelancer dashboard
    path('profile/<int:freelancer_id>/', views.freelancer_profile, name='freelancer-profile'),  # Freelancer profile
    path('edit_profile', views.update_freelancer_profile, name='edit_profile'),  # Edit freelancer profile
    path('viewfreelancer/<int:freelancer_id>/', views.viewfreelancer, name='viewfreelancer'),  # View freelancer as a user
    path('freelancer_list/', views.freelancer_list, name='freelancer-list'),  # List freelancers filtered by profession
    path('submit_comment', views.submit_comment, name='submit_comment'),  # Submit comment
    path('add_comment_to_post', views.add_comment_to_post, name='add_comment_to_post'),
    path('clear_notifications', views.clear_notifications, name='clear_notifications'),
    path('chats', views.view_chats, name='chats'),
    path('set_current_chat/<int:chat_id>/', views.set_current_chat, name='set_current_chat'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
