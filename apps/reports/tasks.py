from __future__ import absolute_import, unicode_literals

import csv
from io import StringIO

from celery import shared_task
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import ReportListResult, Report


def generate_report_list(user_id) -> StringIO:
    """Generate report list body, return save path"""
    fieldnames = (
        'title',
        'user_email',
        'tags',
        'reason',
        'description',
    )

    report_notes = Report.objects \
        .filter(user_id=user_id) \
        .prefetch_related('post', 'user')

    csv_file = StringIO()

    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for report in report_notes:
        data = {
            'title': report.post.title,
            'user_email': report.user.email,
            'tags': ', '.join(report.post.tags.values_list('title')),
            'reason': report.get_reason_display(),
            'description': report.post.description,
        }
        writer.writerow(data)

    return csv_file


@shared_task(bind=True)
def generate_reports(self, user_id: int):
    """Generate and save report data

    Store for download, save file when task finishes running
    """
    task_id = self.request.id

    filename = f"report_{task_id}.csv"

    csv_io = generate_report_list(user_id)
    file = InMemoryUploadedFile(
        file=csv_io,
        field_name="file",
        name=filename,
        content_type=None,
        size=csv_io.tell(),
        charset=None,
    )

    ReportListResult.objects.create(
        task_id=task_id,
        file=file,
        user_id=user_id,
    )


@shared_task(name='delete_old_report_lists')
def delete_old_report_lists():
    """Delete reports which are elder then 1 hour"""
    ReportListResult.objects.outdated_reports().delete()
