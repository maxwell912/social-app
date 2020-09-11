from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.reports.models import Report


@receiver(post_save, sender=Report)
def disable_post(sender, instance, **kwargs):
    """Disable post after 3 reports"""
    post = instance.post
    if post.reports.count() > 2:
        post.disable_view()
