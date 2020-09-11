from django import forms

from apps.tags.models import Tag

__all__ = (
    'TagForm',
)


class TagForm(forms.ModelForm):
    """Form for creating tag"""

    class Meta:
        model = Tag
        fields = ('title', )
