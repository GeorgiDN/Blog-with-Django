from django.contrib.auth.models import User
from django.db import models
from webApp.blog.models import Post


class Like(models.Model):
    to_post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='post_likes',
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_likes',
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('to_post', 'user')


class Comment(models.Model):

    text = models.TextField(
        max_length=300,
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

    class Meta:
        ordering = ['-date_time_of_publication']
