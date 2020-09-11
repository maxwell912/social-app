from django.core.validators import validate_slug
from django.db import models
from django.utils.translation import ugettext_lazy as _

__all__ = (
    'Tag',
)


class Tag(models.Model):
    """Tag model.

    Attributes:
        title (str): Tag's description
        posts (Post): posts with this tag
    """
    posts = models.ManyToManyField(
        'posts.Post',
        related_name='tags',
    )
    title = models.CharField(
        max_length=15,
        unique=True,
        validators=[validate_slug],
        verbose_name=_("Tag's description")
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.title
