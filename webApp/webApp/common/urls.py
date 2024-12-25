from django.urls import path, include
from webApp.common import views

urlpatterns = [
    path('like/<int:post_id>/', views.likes_functionality, name='like'),
    path('comment/<int:post_id>/', views.comments_functionality, name='comment'),
    path('comment/edit/<int:pk>/', views.CommentEditView.as_view(), name='edit_comment'),
]
