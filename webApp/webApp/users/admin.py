from django.contrib import admin
from webApp.users.models import Profile, CustomUser
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')
    list_filter = ('user', 'first_name', 'last_name', 'country', 'city')
    search_fields = ('user__username', 'first_name', 'last_name', 'country', 'city')
    list_per_page = 10
    fieldsets = (
        ('User Profile', {
            'fields': ('user', 'image')
        }),
        ('Name', {
            'fields': ('first_name', 'last_name',),
        }),
        ('Contact', {
            'fields': ('phone',),
        }),
        ('Address', {
            'fields': ('country', 'city', 'address',),
        }),
        ('Company', {
            'fields': ('company',),
        }),
        ('School', {
            'fields': ('school',),
        }),
    )
