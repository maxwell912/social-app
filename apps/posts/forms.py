from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django.core.validators import validate_slug

from .models import Post

__all__ = (
    'PostForm',
    'CommentForm',
    'PostCreateForm',
)


class PostForm(forms.ModelForm):
    """Form for creating post in views"""
    attachments = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
    )

    class Meta:
        model = Post
        fields = (
            'title',
            'description',
        )
        widgets = {
            'title': forms.TextInput(attrs={'type': 'search'}),
        }


class PostCreateForm(PostForm):
    tags = SimpleArrayField(
        forms.CharField(
            max_length=13,
            validators=[validate_slug],
        ),
        delimiter=' ',
        required=False,
        help_text='List of tags separated with " "'
    )


class CommentForm(forms.ModelForm):
    """Form for creating comment in views"""

    class Meta:
        model = Post
        fields = [
            'description',
        ]
