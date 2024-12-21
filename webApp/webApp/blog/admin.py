from django.contrib import admin

from webApp.blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('title', 'date_posted', 'author')

