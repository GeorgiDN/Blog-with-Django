from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message


@login_required
def conversations_list(request):
    user = request.user
    # Get users with whom the user has exchanged messages
    conversations = User.objects.filter(
        Q(sent_messages__recipient=user) | Q(received_messages__sender=user)
    ).distinct()

    context = {
        'conversations': conversations
    }

    return render(request, 'messaging/conversations_list.html', context)


@login_required
def conversation_detail(request, username):
    user = request.user
    recipient = User.objects.get(username=username)

    # Fetch messages exchanged between the two users
    messages = Message.objects.filter(
        Q(sender=user, recipient=recipient) | Q(sender=recipient, recipient=user)
    ).order_by('timestamp')

    messages.filter(recipient=user, is_read=False).update(is_read=True)

    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=user, recipient=recipient, content=content)

    context = {
        'recipient': recipient,
        'messages': messages,
    }

    return render(request, 'messaging/conversation_detail.html', context)
