# standard library imports
import ast
import json

# third party imports

# local imports
from core.celeryapp import app as celery
from core.redisapp import redis


@celery.task
def process_event(event):

	print 'processing_event'

	
	

	