from django.urls import path
from webApp.messaging import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('messages/', views.ConversationsListView.as_view(), name='conversations-list'),
    path('messages/<str:username>/', views.ConversationDetailView.as_view(), name='conversation-detail'),
    path('messages/edit/<int:pk>/', views.MessageEditView.as_view(), name='edit-message'),
    path('messages/delete/<int:pk>/', views.MessageDeleteView.as_view(), name='delete-message'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
