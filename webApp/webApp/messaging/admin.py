from django.contrib import admin

from webApp.messaging.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'is_read', 'timestamp')
    list_filter = ('sender', 'recipient', 'is_read', 'timestamp')
    search_fields = ('sender__username', 'recipient__username', 'is_read', 'timestamp')
    ordering = ('-timestamp',)
    list_per_page = 20
