from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonschema import ValidationError

from apps.posts.models import Post
from apps.users.models import User


__all__ = (
    'BookmarkBase',
    'BookmarkPost',
)


class BookmarkBase(models.Model):
    """Base class of bookmark.

    Fixes a bookmark to a specific user.

    Attribute:
            user (User): The user who owns the bookmark.

    """
    user = models.ForeignKey(
        User,
        verbose_name='User',
        related_name='bookmarks',
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class BookmarkPost(BookmarkBase):
    """Bookmark post model.

    Marks the post as a favorite for the user.

    Attribute:
            post (Post): The post to which the user adds to favorites.

    """
    post = models.ForeignKey(
        Post,
        verbose_name='Post',
        related_name='bookmarks',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'bookmark'
        unique_together = ('user', 'post')

    def clean(self):
        """Forbid adding comments to bookmarks."""
        if self.post.is_comment:
            raise ValidationError(_('Cannot add comment to favorites!'))

    def __str__(self):
        return f'User {self.user.email}: {self.post.title}'
