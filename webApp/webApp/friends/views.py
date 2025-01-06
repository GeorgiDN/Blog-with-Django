from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from .models import Friendship, FriendRequest
from django.contrib.auth.models import User


@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if request.user != to_user:
        FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    return redirect('friend-requests')


# @login_required
# def accept_friend_request(request, request_id):
#     friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
#     from_user = friend_request.from_user
#     to_user = friend_request.to_user
#
#     to_user.friendship.friends.add(from_user)
#     from_user.friendship.friends.add(to_user)
#
#     friend_request.delete()
#     return redirect('friend-requests')


@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    from_user = friend_request.from_user
    to_user = friend_request.to_user

    # Ensure both users have a Friendship object
    if not hasattr(from_user, 'friendship'):
        Friendship.objects.create(user=from_user)
    if not hasattr(to_user, 'friendship'):
        Friendship.objects.create(user=to_user)

    to_user.friendship.friends.add(from_user)
    from_user.friendship.friends.add(to_user)

    friend_request.delete()

    return redirect('friend-requests')



@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        to_user=request.user
    )
    friend_request.delete()
    return redirect('friend-request')


@login_required
def friend_list(request):
    friends = request.user.friendship.friends.all()

    context = {
        'friends': friends
    }

    return render(request, 'friends/friend_list.html', context)


@login_required
def friend_requests(request):
    # Fetch friend requests sent to the current user
    requests_received = FriendRequest.objects.filter(to_user=request.user)

    context = {
        'requests_received': requests_received
    }

    return render(request, 'friends/friend_requests.html', context)
