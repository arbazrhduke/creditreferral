import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'defrag.settings.local')
app = Celery(str('defrag'))
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
