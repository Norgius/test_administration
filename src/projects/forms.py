from django import forms

from .models import Comment


class CommentForm(forms.Form):
    text = forms.CharField(
        label='Комментарий',
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
    )
