from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.urls.base import reverse
from django.views.generic import UpdateView, DeleteView, ListView, DetailView

from .forms import MessageEditForm
from .models import Message


class ConversationsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'messaging/conversations_list.html'
    context_object_name = 'conversations'

    def get_queryset(self):
        user = self.request.user
        return User.objects.prefetch_related('sent_messages', 'received_messages').filter(
            Q(sent_messages__recipient=user) | Q(received_messages__sender=user)
        ).distinct().annotate(
            unread_count=Count(
                'sent_messages',
                filter=Q(sent_messages__recipient=user, sent_messages__is_read=False)
            )
        )


class ConversationDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'messaging/conversation_detail.html'
    context_object_name = 'recipient'

    def get_object(self, **kwargs):
        return User.objects.get(username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        recipient = self.get_object()

        conversation_messages = Message.objects.select_related('sender', 'recipient').filter(
            Q(sender=user, recipient=recipient) | Q(sender=recipient, recipient=user)
        ).order_by('timestamp')

        conversation_messages.filter(recipient=user, is_read=False).update(is_read=True)

        context['conversation_messages'] = conversation_messages
        context['last_message_id'] = conversation_messages.last().pk\
            if conversation_messages.exists() else None
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        recipient = self.get_object()
        content = request.POST.get('content')
        file = request.FILES.get('file')

        if content or file:
            new_message = Message.objects.create(
                sender=user,
                recipient=recipient,
                content=content,
                file=file)

            self.last_message_id = new_message.pk

        return redirect(self.get_success_url())

    def get_success_url(self):
        last_message_id = getattr(self, 'last_message_id', None)
        if last_message_id:
            return reverse('conversation-detail',
                           kwargs={'username': self.get_object().username}) + f"#message-{last_message_id}"
        return reverse('conversation-detail', kwargs={'username': self.get_object().username})


class MessageEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageEditForm
    template_name = 'messaging/edit_message.html'

    def get_success_url(self):
        return (reverse(
            'conversation-detail',
            args=[self.object.recipient.username])
                + f"#message-{self.object.pk}")

    def test_func(self):
        curr_message = self.get_object()
        return curr_message.sender == self.request.user


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'messaging/delete_message.html'

    def get_success_url(self):
        return (reverse(
            'conversation-detail',
            args=[self.object.recipient.username])
                + f"#message-{self.object.pk}")

    def test_func(self):
        curr_message = self.get_object()
        return curr_message.sender == self.request.user


# FBV
# @login_required
# def conversations_list(request):
#     user = request.user
#
#     conversations = User.objects.filter(
#         Q(sent_messages__recipient=user) | Q(received_messages__sender=user)
#     ).distinct().annotate(
#         unread_count=Count(
#             'sent_messages',
#             filter=Q(sent_messages__recipient=user, sent_messages__is_read=False)
#         )
#     )
#
#     context = {
#         'conversations': conversations,
#
#     }
#
#     return render(request, 'messaging/conversations_list.html', context)
#
#
# @login_required
# def conversation_detail(request, username):
#     user = request.user
#     recipient = User.objects.get(username=username)
#
#     # Fetch messages exchanged between the two users
#     conversation_messages = Message.objects.filter(
#         Q(sender=user, recipient=recipient) | Q(sender=recipient, recipient=user)
#     ).order_by('timestamp')
#
#     conversation_messages.filter(recipient=user, is_read=False).update(is_read=True)
#
#     if request.method == "POST":
#         content = request.POST.get('content')
#         if content:
#             Message.objects.create(sender=user, recipient=recipient, content=content)
#
#     context = {
#         'recipient': recipient,
#         'conversation_messages': conversation_messages,
#     }
#
#     return render(request, 'messaging/conversation_detail.html', context)
