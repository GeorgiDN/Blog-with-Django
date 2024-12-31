from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.urls.base import reverse
from django.views.generic import UpdateView

from .forms import MessageEditForm
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

    # Fetch messages exchanged between the two users
    conversation_messages = Message.objects.filter(
        Q(sender=user, recipient=recipient) | Q(sender=recipient, recipient=user)
    ).order_by('timestamp')

    conversation_messages.filter(recipient=user, is_read=False).update(is_read=True)

    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=user, recipient=recipient, content=content)

    context = {
        'recipient': recipient,
        'conversation_messages': conversation_messages,
    }

    return render(request, 'messaging/conversation_detail.html', context)


class MessageEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageEditForm
    template_name = 'messaging/edit_message.html'

    def get_success_url(self):
        return reverse('conversation-detail', args=[self.object.recipient.username]) + f"#message-{self.object.pk}"

    def test_func(self):
        curr_message = self.get_object()
        return curr_message.sender == self.request.user
