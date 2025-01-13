from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from webApp.blocking.models import Block


def get_blocked_users(user):
    return Block.objects.filter(
        Q(blocker=user) |
        Q(blocked=user)
    )


@login_required
def block_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        return HttpResponseBadRequest('You cannot block yourself!')

    Block.objects.get_or_create(blocker=request.user, blocked=target_user)
    return redirect('blocked-users-list', user_id)


@login_required
def unblock_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    Block.objects.filter(blocker=request.user, blocked=target_user).delete()
    return redirect('blocked-users-list', user_id)


@login_required
def blocked_users_list(request, user_id):
    blocked_users = get_blocked_users(request.user)

    context = {
        'blocked_users': blocked_users
    }

    return render(request, 'blocking/blocked_users_list.html', context)
