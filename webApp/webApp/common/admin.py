from django.contrib import admin

from webApp.common.models import Like, Comment


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('to_post', 'to_comment', 'user')
    list_filter = ('to_post', 'to_comment')
    search_fields = ('to_post__title', 'user__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('to_post', 'user')
    list_filter = ('to_post', 'user')
    search_fields = ('to_post__title', 'user__username')
