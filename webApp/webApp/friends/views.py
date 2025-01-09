from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from .models import Friendship, FriendRequest
from django.contrib.auth.models import User


class SendFriendRequestView(LoginRequiredMixin, View):
    model = FriendRequest

    def get_object(self, **kwargs):
        obj = get_object_or_404(
            User,
            id=self.kwargs['user_id'],
        )
        return obj

    def post(self, request, *args, **kwargs):
        to_user = self.get_object()

        if request.user == to_user:
            messages.error(request, "You cannot send a friend request to yourself.")
            return redirect('profile-view', username=to_user.username)

        if Friendship.objects.filter(user=request.user, friends=to_user).exists():
            messages.info(request, f'You are already friends with {to_user.username}.')
            return redirect('profile-view', username=to_user.username)

        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=to_user,
        )

        if created:
            messages.success(request, f'Friend request sent to {to_user.username}.')
        else:
            messages.info(request, f'You have already sent a friend request to {to_user.username}.')

        return redirect('profile-view', username=to_user.username)


class AcceptFriendRequestView(LoginRequiredMixin, SuccessMessageMixin, View):
    model = FriendRequest
    success_url = reverse_lazy('friend-requests')

    def get_object(self, **kwargs):
        obj = get_object_or_404(
            FriendRequest,
            id=self.kwargs['request_id'],
            to_user=self.request.user
        )
        return obj

    def post(self, request, *args, **kwargs):
        friend_request = self.get_object()
        from_user = friend_request.from_user
        to_user = friend_request.to_user

        if not hasattr(from_user, 'friendship'):
            Friendship.objects.create(user=from_user)
        if not hasattr(to_user, 'friendship'):
            Friendship.objects.create(user=to_user)

        to_user.friendship.friends.add(from_user)
        from_user.friendship.friends.add(to_user)

        messages.success(self.request, f'User {from_user.username} is added as a friend.')
        friend_request.delete()

        return redirect(self.success_url)


class RejectFriendRequestView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = FriendRequest
    success_url = reverse_lazy('friend-requests')
    success_message = 'You rejected the friend request'

    def get_object(self, **kwargs):
        obj = get_object_or_404(
            FriendRequest,
            id=self.kwargs['request_id'],
            to_user=self.request.user
        )
        return obj

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        friend_request = self.get_object()
        friend_request.delete()
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)


class FriendListView(LoginRequiredMixin, ListView):
    model = Friendship
    template_name = 'friends/friend_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)

        friendship, created = Friendship.objects.get_or_create(user=user)
        friends = friendship.friends.all()

        context['friends'] = friends
        context['user'] = user
        return context


class FriendRequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = FriendRequest
    template_name = 'friends/friend_requests.html'
    context_object_name = 'requests_received'

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     requests_received = FriendRequest.objects.filter(to_user=self.request.user)
    #     context["requests_received"] = requests_received
    #     return context

    def test_func(self):
        return self.request.user.is_authenticated


class RemoveFriendView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get_object(self):
        return get_object_or_404(User, id=self.kwargs['user_id'])

    def test_func(self):
        user_friend = self.get_object()
        return user_friend in self.request.user.friendship.friends.all()

    def get(self, request, *args, **kwargs):
        user_friend = self.get_object()
        context = {'user_friend': user_friend}
        return render(request, 'friends/remove_friend.html', context)

    def post(self, request, *args, **kwargs):
        user_friend = self.get_object()
        request.user.friendship.friends.remove(user_friend)
        user_friend.friendship.friends.remove(request.user)
        messages.success(request, f'{user_friend.username} is removed from your friends.')
        return redirect('friend-list-user', user_id=request.user.id)

# FBV
# @login_required
# def send_friend_request(request, user_id):
#     to_user = get_object_or_404(User, id=user_id)
#
#     if request.user == to_user:
#         messages.error(request, "You cannot send a friend request to yourself.")
#         return redirect('profile-view', username=to_user.username)
#
#     if Friendship.objects.filter(user=request.user, friends=to_user).exists():
#         messages.info(request, f'You are already friends with {to_user.username}.')
#         return redirect('profile-view', username=to_user.username)
#
#     friend_request, created = FriendRequest.objects.get_or_create(
#         from_user=request.user, to_user=to_user
#     )
#
#     if created:
#         messages.success(request, f'Friend request sent to {to_user.username}.')
#     else:
#         messages.info(request, f'You have already sent a friend request to {to_user.username}.')
#
#     return redirect('profile-view', username=to_user.username)


# @login_required
# def accept_friend_request(request, request_id):
#     friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
#     from_user = friend_request.from_user
#     to_user = friend_request.to_user
#
#     if not hasattr(from_user, 'friendship'):
#         Friendship.objects.create(user=from_user)
#     if not hasattr(to_user, 'friendship'):
#         Friendship.objects.create(user=to_user)
#
#     to_user.friendship.friends.add(from_user)
#     from_user.friendship.friends.add(to_user)
#
#     messages.success(request, f'User {from_user.username} is added as a friend.')
#     friend_request.delete()
#
#     return redirect('friend-requests')


# @login_required
# def reject_friend_request(request, request_id):
#     friend_request = get_object_or_404(
#         FriendRequest,
#         id=request_id,
#         to_user=request.user
#     )
#
#     messages.success(request, 'You rejected the friend request')
#     friend_request.delete()
#     return redirect('friend-requests')


# @login_required
# def friend_list(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     friendship, created = Friendship.objects.get_or_create(user=user)
#     friends = friendship.friends.all()
#
#     context = {
#         'friends': friends,
#         'user': user,
#     }
#
#     return render(request, 'friends/friend_list.html', context)


# @login_required
# def friend_requests(request):
#     requests_received = FriendRequest.objects.filter(to_user=request.user)
#
#     context = {
#         'requests_received': requests_received
#     }
#
#     return render(request, 'friends/friend_requests.html', context)


# @login_required
# def remove_friend(request, user_id):
#     user = request.user
#     user_friend = get_object_or_404(User, id=user_id)
#
#     if request.method == 'POST' and user_friend in request.user.friendship.friends.all():
#         user.friendship.friends.remove(user_friend)
#         user_friend.friendship.friends.remove(user)
#         messages.success(request, f'{user_friend.username} is removed from your friends.')
#         return redirect('friend-list-user', user_id=user.id)
#
#     context = {
#         'user_friend': user_friend,
#         'user': user,
#     }
#
#     return render(request, 'friends/remove_friend.html', context)
