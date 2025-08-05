import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webApp.settings")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
from webApp.blog.models import Post
import random
from webApp.messaging.models import Message


def create_users():
    admin = User.objects.create_user(
        username='admin',
        email='admin@admin.com',
        password='django_2025',
        is_staff=True,
        is_superuser=True
    )
    print(f"Created admin user: {admin.username}")

    # Regular users
    users_data = [
        {
            'username': 'Ivan',
            'email': 'myemail250@proton.me',
            'password': 'django_2025',
            'first_name': 'Ivan',
            'last_name': 'Ivanov'
        },
        {
            'username': 'Ludmila',
            'email': 'myemail260@proton.me',
            'password': 'django_2025',
            'first_name': 'Ludmila',
            'last_name': 'Ludmila'
        },
        {
            'username': 'Pesho',
            'email': 'myemail280@proton.me',
            'password': 'django_2025',
            'first_name': 'Pesho',
            'last_name': 'Peshov'
        }
    ]

    for user_data in users_data:
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', '')
        )
        print(f"Created user: {user.username}")


create_users()

# Create posts and messages
def create_post():
    for i in range(1, 30):
        post = Post()
        post.title = f'Blog {i}'
        post.content = f'Post Content {i} is created'
        id_ = random.choice([2, 3, 4])
        current_author = User.objects.get(pk=id_)
        post.author = current_author
        post.save()
    print("Posts are created")


create_post()


def create_message():
    for i in range(1, 4):
        curr_message = Message()
        curr_message.content = f'Message number {i}'
        recipient_id = 2
        sender_id = 3
        curr_message.sender = User.objects.get(pk=sender_id)
        curr_message.recipient = User.objects.get(pk=recipient_id)
        curr_message.save()

    for i in range(1, 4):
        curr_message = Message()
        curr_message.content = f'Message number {i}'
        recipient_id = 3
        sender_id = 2
        curr_message.sender = User.objects.get(pk=sender_id)
        curr_message.recipient = User.objects.get(pk=recipient_id)
        curr_message.save()


for i in range(6):
    create_message()
