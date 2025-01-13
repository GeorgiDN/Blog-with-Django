from django.urls import path
from webApp.blocking import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('block/<int:user_id>', views.block_user, name='block-user'),
    path('unblock/<int:user_id>', views.unblock_user, name='unblock-user'),
    path('blocklist/<int:user_id>', views.blocked_users_list, name='blocked-users-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
