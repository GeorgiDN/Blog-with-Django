from django.contrib import admin

from webApp.friends.models import Friendship, FriendRequest


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'timestamp')
    list_filter = ('from_user', 'to_user', 'timestamp')
    search_fields = ('from_user__username', 'to_user__username')
    ordering = ('-timestamp',)
    list_per_page = 20


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)
