from django.contrib import admin

from webApp.blocking.models import Block


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    pass
