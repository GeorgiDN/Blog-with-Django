from django.contrib import admin

from webApp.blocking.models import Block


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('blocker', 'blocked', 'created_at')
    list_filter = ('blocker', 'blocked', 'created_at')
