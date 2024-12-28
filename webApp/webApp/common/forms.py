from webApp.common.models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={
                "placeholder": "Add a comment...",
                "rows": 4,
                "cols": 40,
                "class": "form-control",
            }),
        }


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }
        labels = {
            'text': 'Edit your comment',
        }


class SearchForm(forms.Form):
    post_title = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Search by Post title...',
                   'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['post_title'].label = ''
