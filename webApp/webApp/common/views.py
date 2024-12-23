from django.contrib.auth.decorators import login_required

from webApp.common.models import Like
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
