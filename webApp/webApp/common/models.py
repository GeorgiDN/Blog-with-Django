from django.core.exceptions import ValidationError
from django.db import models

from webApp.blog.models import Post
from django.contrib.auth import get_user_model
User = get_user_model()


class Like(models.Model):
    to_post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='post_likes',
        null=True,
        blank=True,
    )
    to_comment = models.ForeignKey(
        to="Comment",
        on_delete=models.CASCADE,
        related_name='comment_likes',
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_likes',
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):
        if not self.to_post and not self.to_comment:
            raise ValidationError("A like must be associated with either a post or a comment.")
        if self.to_post and self.to_comment:
            raise ValidationError("A like cannot be associated with both a post and a comment.")

    def save(self, *args, **kwargs):
        self.clean()  # Call validation before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Like"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['to_post', 'user'],
                name='unique_like_to_post'
            ),
            models.UniqueConstraint(
                fields=['to_comment', 'user'],
                name='unique_like_to_comment'
            )
        ]


class Comment(models.Model):

    text = models.TextField(
        max_length=1000,
    )
    date_time_of_publication = models.DateTimeField(
        auto_now_add=True
    )
    to_post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='post_comments',
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_comments',
    )

    def __str__(self):
        return f'{self.user} comment: {self.to_post}'

    class Meta:
        ordering = ['-date_time_of_publication']
