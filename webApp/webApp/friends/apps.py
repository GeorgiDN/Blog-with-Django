from django.apps import AppConfig


class FriendsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webApp.friends'

    def ready(self):
        import webApp.friends.signals
