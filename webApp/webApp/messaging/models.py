from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from webApp.blocking.views import get_blocked_users


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        User,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField(
        max_length=1000,
    )
    timestamp = models.DateTimeField(
        default=now
    )
    is_read = models.BooleanField(
        default=False
    )
    file = models.FileField(
        upload_to='message_files/',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if self.sender.id in get_blocked_users(self.recipient) or self.recipient.id in get_blocked_users(self.sender):
            raise ValidationError("You cannot send messages to this user.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.timestamp}"
