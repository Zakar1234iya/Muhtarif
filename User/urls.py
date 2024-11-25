from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('profile/<int:id>/', views.user_profile, name='user_profile'),
    path('chat/<int:freelancer_id>/', views.start_chat, name="start_chat"),
    path('send_chat', views.send_chat, name='send_chat'),
    path('create_post', views.create_post, name='create_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('hire_comment', views.hire_comment, name='hire'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
