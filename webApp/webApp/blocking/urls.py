from django.urls import path
from webApp.blocking import views

urlpatterns = [
    path('block/<int:user_id>', views.block_user, name='block-user'),
    path('unblock/<int:user_id>', views.unblock_user, name='unblock-user'),
]
