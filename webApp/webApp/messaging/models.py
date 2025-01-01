from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


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
    content = models.TextField()
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

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.timestamp}"
