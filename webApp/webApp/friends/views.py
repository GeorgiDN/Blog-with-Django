from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Friendship, FriendRequest
from django.contrib.auth.models import User

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Friendship, FriendRequest
from django.contrib.auth.models import User


@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)

    if request.user == to_user:
        messages.error(request, "You cannot send a friend request to yourself.")
        return redirect('profile-view', username=to_user.username)

    if Friendship.objects.filter(user=request.user, friends=to_user).exists():
        messages.info(request, f'You are already friends with {to_user.username}.')
        return redirect('profile-view', username=to_user.username)

    friend_request, created = FriendRequest.objects.get_or_create(
        from_user=request.user, to_user=to_user
    )

    if created:
        messages.success(request, f'Friend request sent to {to_user.username}.')
    else:
        messages.info(request, f'You have already sent a friend request to {to_user.username}.')

    return redirect('profile-view', username=to_user.username)


@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    from_user = friend_request.from_user
    to_user = friend_request.to_user

    if not hasattr(from_user, 'friendship'):
        Friendship.objects.create(user=from_user)
    if not hasattr(to_user, 'friendship'):
        Friendship.objects.create(user=to_user)

    to_user.friendship.friends.add(from_user)
    from_user.friendship.friends.add(to_user)

    messages.success(request, f'User {from_user.username} is added as a friend.')
    friend_request.delete()

    return redirect('friend-requests')


@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        to_user=request.user
    )

    messages.success(request, f'You rejected the friend request')
    friend_request.delete()
    return redirect('friend-requests')


@login_required
def friend_list(request, user_id=None):
    target_user = get_object_or_404(User, id=user_id) if user_id else request.user

    friendship, created = Friendship.objects.get_or_create(user=target_user)
    friends = friendship.friends.all()

    context = {
        'friends': friends,
        'target_user': target_user,  # Pass the target user to the template
    }

    return render(request, 'friends/friend_list.html', context)


@login_required
def friend_requests(request):
    requests_received = FriendRequest.objects.filter(to_user=request.user)

    context = {
        'requests_received': requests_received
    }

    return render(request, 'friends/friend_requests.html', context)
