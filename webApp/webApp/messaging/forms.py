from django import forms

from webApp.messaging.models import Message


class MessageEditForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'cols': 30}),
        }
        labels = {
            'text': 'Edit your message',
        }
