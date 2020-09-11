from django import forms

from apps.reactions.models import Reaction

__all__ = (
    'ReactionForm',
)


class ReactionForm(forms.ModelForm):
    """Form for creating reaction"""

    class Meta:
        model = Reaction
        fields = ('description',)
