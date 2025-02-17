from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.functions.comparison import Coalesce
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q, Count, Max, ExpressionWrapper, F, When, Case
from django.urls.base import reverse
from django.views.generic import UpdateView, DeleteView, ListView, DetailView
from .forms import MessageEditForm
from .models import Message
from ..blocking.views import get_blocked_users
from django.contrib.auth import get_user_model
User = get_user_model()


class ConversationsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'messaging/conversations_list.html'
    context_object_name = 'conversations'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user

        return User.objects.filter(
            Q(sent_messages__recipient=user) | Q(received_messages__sender=user)
        ).distinct().annotate(
            last_message_time=Coalesce(
                Max('sent_messages__timestamp', filter=Q(sent_messages__recipient=user)),
                Max('received_messages__timestamp', filter=Q(received_messages__sender=user))
            ),
            unread_count=Count(
                'sent_messages',
                filter=Q(sent_messages__recipient=user, sent_messages__is_read=False)
            )
        ).order_by('-last_message_time')


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

        last_message = conversation_messages.last()
        last_message_id = last_message.pk if last_message else None

        is_blocked_user = user.id in get_blocked_users(recipient) or recipient.id in get_blocked_users(user)

        context['is_blocked_user'] = is_blocked_user
        context['conversation_messages'] = conversation_messages
        context['last_message_id'] = conversation_messages.last().pk\
            if conversation_messages.exists() else None

        self.last_message_id = last_message_id

        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        recipient = self.get_object()
        content = request.POST.get('content')
        file = request.FILES.get('file')

        is_blocked_user = user.id in get_blocked_users(recipient) or recipient.id in get_blocked_users(user)
        if is_blocked_user:
            return HttpResponseForbidden("You cannot send messages to this user.")

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
        # return (reverse(
        #     'conversation-detail',
        #     args=[self.object.recipient.username])
        #         + f"#message-{self.object.pk}")
        return reverse('conversation-detail', kwargs={'username': self.object.recipient.username})

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
