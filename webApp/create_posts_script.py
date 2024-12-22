import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webApp.settings")
django.setup()

from django.contrib.auth.models import User
from webApp.blog.models import Post
import random


def create_post():
    for i in range(1, 30):
        post = Post()
        post.title = f'Blog {i}'
        post.content = f'Post Content {i} is created'
        id_ = random.choice([2, 3])
        current_author = User.objects.get(pk=id_)
        post.author = current_author
        post.save()
    print("Done")


create_post()
