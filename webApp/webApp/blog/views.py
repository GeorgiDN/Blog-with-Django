from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.models import User
from webApp.blog.models import Post
from webApp.common.models import Like
from webApp.common.forms import CommentForm, SearchForm
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage
from django.conf import settings


class BaseView(LoginRequiredMixin):
    def get_user_liked_posts(self):
        if self.request.user.is_authenticated:
            return Like.objects.filter(user=self.request.user).values_list('to_post_id', flat=True)
        return []

    def get_user_liked_comments(self):
        if self.request.user.is_authenticated:
            return Like.objects.filter(user=self.request.user).values_list('to_comment_id', flat=True)
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_liked_posts'] = self.get_user_liked_posts()
        context['user_liked_comments'] = self.get_user_liked_comments()
        context["search_form"] = SearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('search_term')

        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(content__icontains=search_term) |
                Q(author__username__icontains=search_term)
            )

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
        # return super().form_valid(form)
        response = super().form_valid(form)

        recipient_emails = User.objects.exclude(id=self.request.user.id).values_list('email', flat=True)

        if recipient_emails:
            subject = f'New post Created {form.instance.title}'
            message = (f"Hello,\n\nA new post titled '{form.instance.title}' has been created "
                       f"by {self.request.user.username}. Check it out!")
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER ,
                bcc=recipient_emails,
            )
            email.send(fail_silently=False)
        return response


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
