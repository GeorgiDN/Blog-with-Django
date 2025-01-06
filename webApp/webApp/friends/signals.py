from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Friendship


@receiver(post_save, sender=User)
def create_friendship(sender, instance, created, **kwargs):
    if created:
        Friendship.objects.create(user=instance)
