# standard library imports
from __future__ import absolute_import
import os

# third party imports
from django.conf import settings
from celery import Celery

# local imports


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mm_api.settings')

app = Celery('mm_api', broker=settings.CONSUMER_URL)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
