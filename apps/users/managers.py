from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _

__all__ = (
    'UserManager',
)


class UserManager(BaseUserManager):
    """Custom user manager.

    The custom user manager needs instead base manager because we use
    ``email`` instead ``username`` for authentication.

    """

    def create_user(self, email, password=None):
        """Create user.

        Overridden base user manager method, customized for auth with email
        instead username.

        """

        if not email:
            raise ValueError(_("Users must have an email address!"))

        user = self.model(email=self.normalize_email(email),)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create superuser.

        Overridden base user manager method, customized for auth with email
        instead username.

        """
        user = self.create_user(email, password=password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
