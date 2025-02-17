from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.conf import settings
from webApp.users.validators import PhoneValidator


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    image = models.ImageField(
        default='default.jpg',
        upload_to='profile_pics'
    )
    first_name = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    email_address = models.EmailField(
        null=True,
        blank=True,
        help_text='Here you can share your email'
    )
    phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[PhoneValidator()]
    )
    company = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    school = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    address = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
