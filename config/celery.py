import os

from celery import Celery

from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery(
    'social_app',
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'remove_old_report_lists': {
        'task': 'delete_old_report_lists',
        'schedule': crontab(minute=0),
    },
}