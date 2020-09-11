from typing import List, Tuple
import pathlib

from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from ..reactions.models import Reaction
from ..tags.models import Tag
from config.settings import base
from .managers import PostManager

__all__ = (
    'Post',
    'AttachmentsResult',
)


class Post(models.Model):
    """Post model.

    Attributes:
        user_id (str): Id of user wrote post.
        parent_id (str): Id of post for whom is a comment.
        description (str): Description.
        title (str): Title.
        created_at (date): Date of post creation.
        deleted_at (date): Date of post deleting.
        comment_allowed (bool): Post can be commented.
        is_comment (bool): Post is a comment.
        is_active (bool): Can be seen by users

    """

    user = models.ForeignKey(
        'users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='posts',
    )
    parent_post = models.ForeignKey(
        'posts.Post',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    description = models.TextField(
        max_length=255,
        verbose_name=_("Description"),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date of creation"),
    )
    deleted_at = models.DateTimeField(
        null=True,
        verbose_name=_("Date of deleting"),
    )
    comment_allowed = models.BooleanField(
        default=True,
        verbose_name=_("Post can be commented"),
    )
    is_comment = models.BooleanField(
        default=False,
        verbose_name=_("Post is a comment"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active"),
    )

    objects = PostManager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title

    def add_comment(self, comment: 'Post'):
        """Mark it as 'comment' as comment for current post and

        set same title.
        """
        comment.parent_post = self
        comment.is_comment = True
        comment.title = self.title
        comment.save()

    @property
    def bookmarks_count(self):
        """Return number of bookmarks for post."""
        return self.bookmarks.count()

    def get_reaction_counter(self) -> List[Tuple[str, int]]:
        """Return reaction image urls with count of reactions on post"""
        counter = self.reactions\
            .values('description')\
            .annotate(count=Count('description'))\
            .filter(count__gt=0)
        return [
            (Reaction.IMAGE_URLS[reaction['description']], reaction['count'])
            for reaction in counter
        ]

    def active_comments(self):
        """Return active comments"""
        return self.comments.filter(
            is_active=True,
        )

    def disable_view(self):
        """Disable post for not-staff users(is_active -> False)

        Post can be seen by staff users
        """
        self.is_active = False
        self.save()

    def activate_view(self):
        """Activate post for all users (is_active -> True)

        Post can be seen by all users
        """
        self.is_active = True
        self.save()

    @property
    def comments_count(self):
        """Return count comments for post."""
        return self.comments.count()

    def add_tag(self, title):
        """Create and add tag to post."""
        tag, _ = Tag.objects.get_or_create(title=title)
        self.tags.add(tag)


class AttachmentsResult(models.Model):
    """Temporary records of async task_id, the results as url and filename.

    Specifies the post to save attachments .
    """

    PATH = pathlib.Path(base.MEDIA_ROOT) / 'attachments'

    task_id = models.CharField(
        max_length=255,
        verbose_name=_('Task id'),
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE
    )
    zip_file = models.FileField(
        upload_to='media/attachments',
        verbose_name=_('Zip file'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created_at")
    )

    class Meta:
        ordering = ('created_at',)

        verbose_name = _("Attachments")
        verbose_name_plural = _("Attachments")