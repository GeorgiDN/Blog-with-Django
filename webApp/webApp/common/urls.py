from django.urls import path, include
from webApp.common import views

urlpatterns = [
    path('like/<int:post_id>/', views.likes_functionality, name='like'),
    path('like-comment/<int:comment_id>/', views.likes_to_comment_functionality, name='like-comment'),
    path('comment/new/<int:post_id>/', views.CommentCreateView.as_view(), name='comment'),
    path('comment/edit/<int:pk>/', views.CommentEditView.as_view(), name='edit_comment'),
    path('comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='delete_comment'),
]
