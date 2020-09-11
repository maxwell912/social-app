from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User

__all__ = (
    'CustomUserChangeForm',
    'CustomUserCreationForm',
    'UserProfileForm',
)


class CustomUserChangeForm(UserChangeForm):
    """Custom change form for ``User`` model.

    This class overrides ``UserChangeForm`` to provide different ``User``
    model in Meta.

    """

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'avatar',
            'birthday',
            'gender',
        )


class CustomUserCreationForm(UserCreationForm):
    """Custom creation form for ``User`` model.

    This class overrides ``UserCreationForm`` to provide different ``User``
    model in Meta and also replaces ``username`` field with ``email`` field.

    """

    class Meta:
        model = User
        fields = ('email',)


class UserProfileForm(forms.ModelForm):
    """Form for creating user in views"""

    class Meta:
        model = User
        fields = (
            'email',
            'phone_number',
            'first_name',
            'last_name',
        )
