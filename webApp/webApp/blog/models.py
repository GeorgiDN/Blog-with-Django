from django.db import models
from django.urls.base import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


class Post(models.Model):
    title = models.CharField(
        max_length=100
    )
    content = models.TextField(
        max_length=1000
    )
    date_posted = models.DateTimeField(
        default=timezone.now,
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_posts',
    )
    image = models.ImageField(
        upload_to='post_images',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
