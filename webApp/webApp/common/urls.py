from django.urls import path, include
from webApp.common import views

urlpatterns = [
    path('like/<int:post_id>/', views.likes_functionality, name='like'),
]
