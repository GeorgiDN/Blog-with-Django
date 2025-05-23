"""
URL configuration for webApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from webApp.users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

from webApp.users.views import ProfileDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.AppUserRegisterView.as_view(), name='register'),
    path('profile/', user_views.ProfileView.as_view(), name='profile'),
    path('update-password/', user_views.update_password, name='update-password'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/<int:pk>/', include([
        path('delete/', user_views.ProfileDeleteView.as_view(), name='profile-delete'),
    ])),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'
         ),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'
         ),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'
         ),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'
         ),
    path('', include('webApp.blog.urls')),
    path('common/', include('webApp.common.urls')),
    path('profile/remove-image/', user_views.ConfirmRemoveImageView.as_view(), name='confirm_remove_image'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile-view'),
    path('users-list/', user_views.UsersListView.as_view(), name='users-list'),
    path('messaging/', include('webApp.messaging.urls')),
    path('friends/', include('webApp.friends.urls')),
    path('block/', include('webApp.blocking.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
