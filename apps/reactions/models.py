from pathlib import Path

from django.db import models
from django.utils.translation import ugettext_lazy as _

__all__ = (
    'Reaction',
)


class Reaction(models.Model):
    """Reaction model.

    Attributes:
        description (str): Reaction description
        user (User): Reaction owner
        post (Post):  The post to which the reaction is attached.

    """
    IMAGE_URL = Path('reactions')

    LIKE = 'LK'
    LOVE = 'LV'
    HAHA = 'HA'
    WOW = 'WW'
    SAD = 'SD'
    ANGRY = 'AN'
    IMAGE_URLS = {
        LIKE: str(IMAGE_URL / 'like.png'),
        LOVE: str(IMAGE_URL / 'love.png'),
        HAHA: str(IMAGE_URL / 'haha.png'),
        WOW: str(IMAGE_URL / 'wow.png'),
        SAD: str(IMAGE_URL / 'sad.png'),
        ANGRY: str(IMAGE_URL / 'angry.png'),
    }
    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (LOVE, 'Love'),
        (HAHA, 'Haha'),
        (WOW, 'Wow'),
        (ANGRY, 'Angry'),
        (SAD, 'Sad'),
    ]
    description = models.CharField(
        max_length=2,
        choices=REACTION_CHOICES,
        verbose_name=_("Reaction's description"),
    )
    user = models.ForeignKey(
        'users.User',
        related_name='reactions',
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        'posts.Post',
        related_name='reactions',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ['user', 'post', 'description']

        verbose_name = _("Reaction")
        verbose_name_plural = _("Reactions")

    def __str__(self):
        return self.get_description_display()
