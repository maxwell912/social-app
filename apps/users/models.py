from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from PIL import Image

from ..posts.models import Post
from ..reactions.models import Reaction
from .managers import UserManager

__all__ = (
    'User',
)


_MAX_SIZE = 300
"""Optimal avatar size for profile form."""


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model.

    Attributes:
        first_name (str): First name.
        last_name (str): Last, family name.
        email (str): E-mail, uses for authentication.
        is_active (bool): Can user log in to the system.
        is_staff (bool): Can user access to admin interface.
        date_joined (datetime): Date when the account was created.
        phone (int) : User's phone number.
        avatar () : User's photo.
        birthday (date) : User's date of birth.
        gender (str) : Gender

    Nested attributes:
        is_superuser (bool): The user can super access to admin UI.
        groups(Manager): The groups this user belongs to.
        user_permissions(Manager): Specified permissions for this user.
        last_login (datetime): Last date when user login to the system.

    """
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    GENDER = models.TextChoices('GENDER', 'MALE FEMALE')

    username = models.CharField(
        max_length=255,
        verbose_name=_("Username")
    )
    first_name = models.CharField(
        max_length=255,
        verbose_name=_("First name")
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name=_("Last name")
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_("Email")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active"),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("Is staff"),
        help_text=_("The user will have access to admin interface."),
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Date joined"),
    )
    phone_number = models.CharField(
        max_length=12,
        verbose_name='Phone number',
        null=True,
        blank=True,
        help_text=_("Users phone number.")
    )
    avatar = models.ImageField(
        upload_to='static/imagination',
        verbose_name='Avatar',
        null=True,
        blank=True,
        help_text=_("Users profile photo.")

    )
    birthday = models.DateField(
        verbose_name='Birthday',
        null=True,
        blank=True,
        help_text=_("User's date of birth.")
    )
    gender = models.CharField(
        max_length=255,
        verbose_name='Gender',
        null=True,
        blank=True,
        choices=GENDER.choices,
        help_text=_("User gender.")
    )
    objects = UserManager()

    class Meta:
        db_table = 'users'
        ordering = ('email',)
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = '{first_name} {last_name}'.format(
            first_name=self.last_name,
            last_name=self.first_name,
        )

        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def add_reaction(self, post_id: int, reaction: Reaction):
        """Try to add reaction to post.

        Return False if already exist
        """
        if self.reactions.filter(
                description=reaction.description,
                post_id=post_id,
        ).first():
            return False
        reaction.user = self
        reaction.save()
        return True

    def get_admin_change_url(self) -> str:
        """Get admin change URL.

        Build full url (host + path) to standard Django admin page for
        object like:

            https://api.sitename.com/admin/users/user/234/

        """

        assert self.id, "Instance must have an ID"

        return urljoin(
            settings.DJANGO_SITE_BASE_HOST,
            reverse('admin:users_user_change', args=(self.id,)),
        )

    def save(self, *args, **kwargs):
        """Save the image at the desired size, if required."""
        super(User, self).save(*args, **kwargs)
        if self.avatar:
            resize_avatar(self.avatar)


def resize_avatar(avatar):
    """Resize the image."""
    width = avatar.width
    height = avatar.height
    max_size = max(width, height)
    if max_size > _MAX_SIZE:
        image = Image.open(avatar.path)
        image = image.resize(
            (
                round(width / max_size * _MAX_SIZE),
                round(height / max_size * _MAX_SIZE)),
            Image.ANTIALIAS
        )
        image.save(avatar.path)
