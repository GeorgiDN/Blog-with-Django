from django.contrib import admin

from webApp.blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('title', 'date_posted', 'author')
    search_fields = ('title', 'author__username')
    ordering = ['-date_posted']
    list_per_page = 20
