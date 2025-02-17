from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from webApp.blocking.models import Block
from django.contrib.auth import get_user_model
User = get_user_model()


def get_blocked_users(user):
    blocked_users = Block.objects.filter(
        Q(blocker=user) |
        Q(blocked=user)
    )

    blocked_user_ids = set(
        blocked_users.values_list('blocker__id', flat=True).union(
            blocked_users.values_list('blocked__id', flat=True)
        )
    )

    blocked_user_ids.discard(user.id)
    return blocked_user_ids


@login_required
def block_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        return HttpResponseBadRequest('You cannot block yourself!')

    Block.objects.get_or_create(blocker=request.user, blocked=target_user)
    return redirect('blocked-users-list')


@login_required
def unblock_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    Block.objects.filter(blocker=request.user, blocked=target_user).delete()
    return redirect('blocked-users-list')


@login_required
def blocked_users_list(request):
    my_blocked_users_list = User.objects.filter(
        id__in=Block.objects.filter(blocker=request.user).values_list('blocked', flat=True)
    )

    context = {
        'my_blocked_users_list': my_blocked_users_list
    }

    return render(request, 'blocking/blocked_users_list.html', context)
