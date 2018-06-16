# standard library imports
import ast
import json

# third party imports

# local imports
from core.celery import app as celery


@celery.task
def process_event():

	print 'processing_event'

	