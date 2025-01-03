from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.models import User
from webApp.blog.models import Post
from webApp.common.models import Like
from webApp.common.forms import CommentForm, SearchForm


def home(request):
    posts = Post.objects.all()

    context = {
        'posts': posts
    }

    return render(request, 'blog/home.html', context)


class BaseView(LoginRequiredMixin):
    def get_user_liked_posts(self):
        if self.request.user.is_authenticated:
            return Like.objects.filter(user=self.request.user).values_list('to_post_id', flat=True)
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_liked_posts'] = self.get_user_liked_posts()
        context["search_form"] = SearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        post_title = self.request.GET.get('post_title')

        if post_title:
            queryset = queryset.filter(title__icontains=post_title)

        return queryset


class PostListView(BaseView, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(BaseView, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(BaseView, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
