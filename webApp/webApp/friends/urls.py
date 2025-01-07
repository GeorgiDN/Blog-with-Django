from django.urls import path
from . import views

urlpatterns = [
    path('send-request/<int:user_id>/', views.send_friend_request, name='send-friend-request'),
    path('accept-request/<int:request_id>/', views.accept_friend_request, name='accept-friend-request'),
    path('reject-request/<int:request_id>/', views.reject_friend_request, name='reject-friend-request'),
    path('friends/<int:user_id>/', views.friend_list, name='friend-list-user'),
    path('requests/', views.friend_requests, name='friend-requests'),
]
