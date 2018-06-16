# standard library imports
import ast
import json

# third party imports

# local imports
from core.celeryapp import app as celery


@celery.task
def process_event(event):

	print 'processing_event'

	