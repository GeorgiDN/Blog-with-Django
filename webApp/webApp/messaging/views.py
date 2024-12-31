from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from .models import Message


@login_required
def conversations_list(request):
    user = request.user

    conversations = User.objects.filter(
        Q(sent_messages__recipient=user) | Q(received_messages__sender=user)
    ).distinct().annotate(
        unread_count=Count(
            'sent_messages',
            filter=Q(sent_messages__recipient=user, sent_messages__is_read=False)
        )
    )

    context = {
        'conversations': conversations,

    }

    return render(request, 'messaging/conversations_list.html', context)


@login_required
def conversation_detail(request, username):
    user = request.user
    recipient = User.objects.get(username=username)
    sender = User.objects.get(username=username)

    # Fetch messages exchanged between the two users
    conversation_messages = Message.objects.filter(
        Q(sender=user, recipient=recipient) | Q(sender=recipient, recipient=user)
    ).order_by('timestamp')

    conversation_messages.filter(recipient=user, is_read=False).update(is_read=True)

    incoming_messages = Message.objects.filter(Q(sender=recipient, recipient=user))
    sent_messages = Message.objects.filter(Q(sender=recipient, recipient=user))

    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=user, recipient=recipient, content=content)

    context = {
        'recipient': recipient,
        'conversation_messages': conversation_messages,
        'incoming_messages': incoming_messages,
        'sent_messages': sent_messages
    }

    return render(request, 'messaging/conversation_detail.html', context)
