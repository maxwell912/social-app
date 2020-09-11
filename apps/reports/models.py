import pathlib
import time

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.reports.managers import ReportListManager
from config.settings import base

__all__ = (
    'Report',
    'ReportListResult',
)


class Report(models.Model):
    """Report model.

    Attributes:
        user_id (str): Id of user wrote report.
        post_id (str): Reported post.
        reason (str): Report reason.
        created_at (date): Date of post creation.

    """
    SPAM = 'SR'
    HARASSMENT = 'HR'
    VIOLENCE = 'VL'
    EXTREMISM = 'EX'
    REPORT_REASON_CHOICES = [
        (SPAM, 'Spam'),
        (HARASSMENT, 'Harassment'),
        (VIOLENCE, 'Violence'),
        (EXTREMISM, 'Extremism'),
    ]

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='reports'
    )
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='reports'
    )
    reason = models.CharField(
        max_length=2,
        choices=REPORT_REASON_CHOICES,
        verbose_name=_("Report body")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date of creation"),
    )

    class Meta:
        ordering = ('-created_at',)
        unique_together = ['user', 'post']

        verbose_name = _("Report")
        verbose_name_plural = _("Reports")


def get_upload_path(instance, filename):
    return (
        pathlib.Path('reports') /
        str(instance.user_id) /
        f'{time.time()}_{filename}'
    )


class ReportListResult(models.Model):
    """ReportList result model.

    Attributes:
        task_id (str): Celery id of task.
        user (str): user who requested the task.
        url (str): url for task result file.
        created_at (date): Date of result file creation.
    """
    REPORT_PATH = pathlib.Path(base.MEDIA_ROOT) / 'reports'

    task_id = models.CharField(
        max_length=255,
        verbose_name=_("task_id"),
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to=get_upload_path,
        verbose_name=_("result_url"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created_at")
    )

    objects = ReportListManager()

    class Meta:
        ordering = ('created_at',)

        verbose_name = _("Report list")
        verbose_name_plural = _("Reports lists")
