from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author': 'George',
        'title': 'My First Post',
        'content': 'This is my first blog post!',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Ivan',
        'title': 'My Second Post',
        'content': 'This is my second blog post!',
        'date_posted': 'April 20, 2019'
    },

]


def home(request):

    context = {
        'posts': posts
    }

    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
