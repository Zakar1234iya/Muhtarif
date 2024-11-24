from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('profile/<int:id>/', views.user_profile, name='user_profile'),
    path('chat', views.chat, name="chat"),
    path('create_post', views.create_post, name='create_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('hire_comment/<int:comment_id>/', views.hire_comment, name='hire_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
