from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'we_market.settings')

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

app = Celery('we_market', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task
def add(x,y):
    return x+y
