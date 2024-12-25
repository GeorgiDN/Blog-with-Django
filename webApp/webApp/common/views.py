from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls.base import reverse
from django.views.generic import UpdateView

from webApp.blog.models import Post
from webApp.common.forms import CommentForm, CommentEditForm
from webApp.common.models import Like, Comment
from django.shortcuts import redirect


@login_required
def likes_functionality(request, post_id: int):
    liked_object = Like.objects.filter(to_post_id=post_id, user=request.user).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_post_id=post_id, user=request.user)
        like.save()

    return redirect(request.META['HTTP_REFERER'] + f'#{post_id}')


@login_required
def comments_functionality(request, post_id: int):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_post = post
            comment.user = request.user
            comment.save()

    return redirect(f"{request.META.get('HTTP_REFERER')}#comments-{post_id}")
    # return redirect(request.META.get("HTTP_REFERER") + f"#{post_id}")


class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentEditForm
    template_name = 'blog/edit-comment.html'

    def get_success_url(self):
        """Redirect to the post detail page with the comments section visible."""
        post_id = self.object.to_post.id
        return reverse('post-detail', args=[post_id]) + f"#comments-{post_id}"

    def test_func(self):
        """Check if the logged-in user is the owner of the comment."""
        comment = self.get_object()
        return comment.user == self.request.user
