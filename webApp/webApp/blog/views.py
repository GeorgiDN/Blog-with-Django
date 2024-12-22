from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from webApp.blog.models import Post


def home(request):
    posts = Post.objects.all()

    context = {
        'posts': posts
    }

    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
