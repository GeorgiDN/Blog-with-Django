from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls.base import reverse
from django.views.generic import UpdateView, DeleteView, View

from webApp.blog.models import Post
from webApp.common.forms import CommentForm, CommentEditForm
from webApp.common.models import Like, Comment
from django.shortcuts import redirect, get_object_or_404


@login_required
def likes_to_comment_functionality(request, comment_id: int):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.to_post_id
    liked_object = Like.objects.filter(to_comment_id=comment_id, user=request.user).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_comment_id=comment_id, user=request.user)
        like.save()

    return redirect(f"{request.META['HTTP_REFERER']}#comments-{post_id}")


@login_required
def likes_functionality(request, post_id: int):
    liked_object = Like.objects.filter(to_post_id=post_id, user=request.user).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_post_id=post_id, user=request.user)
        like.save()

    return redirect(request.META['HTTP_REFERER'] + f'#{post_id}')


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_id)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_post = post
            comment.user = request.user
            comment.save()

        return redirect(f"{request.META.get('HTTP_REFERER')}#comments-{post_id}")


class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentEditForm
    template_name = 'common/edit-comment.html'

    def get_success_url(self):
        """Redirect to the post detail page with the comments section visible."""
        post_id = self.object.to_post.id
        return reverse('post-detail', args=[post_id]) + f"#comments-{post_id}"

    def test_func(self):
        """Check if the logged-in user is the owner of the comment."""
        comment = self.get_object()
        return comment.user == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'common/delete-comment.html'

    def get_success_url(self):
        post_id = self.object.to_post.id
        return reverse('post-detail', args=[post_id]) + f"#comments-{post_id}"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user
