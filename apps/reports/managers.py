from datetime import timedelta

from django.db.models import Manager
from django.utils import timezone


class ReportListManager(Manager):
    """Manager to filter report lists"""

    def outdated_reports(self):
        """Return reports which are elder than 1 hour"""
        filter_date = timezone.now() - timedelta(hours=1)
        return self.filter(
            created_at__lte=filter_date,
        )
