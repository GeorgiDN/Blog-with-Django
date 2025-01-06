from django.db import models
from django.contrib.auth.models import User


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friend_requests_sent',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friend_requests_received',
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'{self.from_user} -> {self.to_user}'


class Friendship(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='friendship',
    )
    friends = models.ManyToManyField(
        User,
        related_name='friend_of',
        blank=True,
        null=True,
    )
