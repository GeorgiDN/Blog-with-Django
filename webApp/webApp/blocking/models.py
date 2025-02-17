from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


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

    def __str__(self):
        return f'User {self.blocker} block User {self.blocked}'
