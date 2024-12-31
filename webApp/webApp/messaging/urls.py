from django.urls import path
from webApp.messaging import views

urlpatterns = [
    path('messages/', views.conversations_list, name='conversations-list'),
    path('messages/<str:username>/', views.conversation_detail, name='conversation-detail'),
    path('messages/edit/<int:pk>/', views.MessageEditView.as_view(), name='edit-message'),
]
