import pathlib

from django.db import models
from django.utils.translation import ugettext_lazy as _

__all__ = (
    'File',
)


def get_upload_path(instance, filename):
    return (
        pathlib.Path('post_attachments') /
        str(instance.post_id) /
        f'{instance.post.attachments.count()}_{filename}'
    )


class File(models.Model):
    """File model.

    Attributes:
        file (File): file
        post (Post):  The post to which the file is attached.

    """
    file = models.FileField(
        upload_to=get_upload_path,
        verbose_name=_("File"),
    )
    post = models.ForeignKey(
        'posts.Post',
        related_name='attachments',
        on_delete=models.CASCADE
    )

    image_suffixes = ['.png', '.jpeg']

    def is_image(self) -> bool:
        """Unsure file is image by suffix"""
        filename = self.file.name
        path = pathlib.Path(filename)
        suffix = path.suffix.lower()
        return suffix in File.image_suffixes

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")
