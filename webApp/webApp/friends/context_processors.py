from webApp.friends.models import FriendRequest


def requests_count(request):
    if request.user.is_authenticated:
        friend_requests = FriendRequest.objects.filter(to_user=request.user).count()
        return {'requests_count': friend_requests}
    return {'requests_count': 0}
