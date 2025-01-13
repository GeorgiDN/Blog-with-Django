from django.contrib.auth.models import User
from django.db import models


class Block(models.Model):
    blocker = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='blocking',
    )
    blocked = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='blocked',
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('blocker', 'blocked')
