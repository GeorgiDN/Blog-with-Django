from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('send-request/<int:user_id>/', views.send_friend_request, name='send-friend-request'),
    path('accept-request/<int:request_id>/', views.AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('reject-request/<int:request_id>/', views.RejectFriendRequestView.as_view(), name='reject-friend-request'),
    path('friends/<int:user_id>/', views.FriendListView.as_view(), name='friend-list-user'),
    path('requests/', views.FriendRequestListView.as_view(), name='friend-requests'),
    path('remove/<int:user_id>/', views.RemoveFriendView.as_view(), name='remove-friend'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
