from django.db.models import Manager, Count, Value
from django.forms import BooleanField


class PostManager(Manager):
    """Manager to filter posts"""

    def active_posts(self):
        """Return active posts"""
        return self.filter(is_active=True)

    def disabled_posts(self):
        """Return disables posts"""
        return self.filter(is_active=False)

    def feed(self):
        """Return active non-comment posts"""
        return (
            self.filter(is_comment=False, is_active=True)
                .annotate(
                    reaction_count=Count('reactions'),
                    comment_count=Count('comments'),
                )
        )

    def user_favorite(self, user_id: int):
        """Return posts which are in user bookmarks"""
        return (
            self.feed()
                .filter(
                bookmarks__user_id=user_id,
            )
        )
