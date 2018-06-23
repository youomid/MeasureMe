# standard library imports
import ast
import json

# third party imports
from channels import Group
from django.conf import settings
import requests

# local imports
from core.celeryapp import app as celery
from core.redisapp import redis


@celery.task
def process_event(event):
	# TODO: use channels consumer to send messages directly
	event = json.loads(event)
	payload = {
		"date": str(event['date']) + " minutes ago",
		"title": event['title'],
		"description": event['description']
	}
	headers = {
		'Authorization': "Token " + settings.API_TOKEN
	}
	print requests.post(url="http://localhost:8000/events/", data=payload, headers=headers).content


	