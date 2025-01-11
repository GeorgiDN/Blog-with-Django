import os

from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User


@shared_task
def send_email_to_users(post_title, post_content, author_username):
    from webApp.celery import app
    if author_username == 'admin':
        recipient_emails = User.objects.exclude(username=author_username).values_list('email', flat=True)
        if recipient_emails:
            subject = f"Important: {post_title}"
            message = f"Hi,\n\nNew message:\n {post_content}"
            send_mail(
                subject=subject,
                message=message,
                from_email=os.environ['EMAIL_HOST_USER'],
                recipient_list=recipient_emails,
                fail_silently=False,
            )
