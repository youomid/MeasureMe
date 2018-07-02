# standard library imports
import ast
import json
from datetime import datetime

# third party imports
from channels import Group
from django.conf import settings
import requests

# local imports
from core.celeryapp import app as celery
from core.redisapp import redis
from processing.models import Event


@celery.task
def process_event(event):

	event = json.loads(event)

	Event.objects.create(
		user_name=event['user'],
		date=datetime.strptime(event['date'], "%Y-%m-%dT%H:%M:%S",
		title=event['title'],
		description=event['description']
		)
	


	