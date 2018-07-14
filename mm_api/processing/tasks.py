# standard library imports
import ast
import json
import time
import pytz
from datetime import datetime

# third party imports
from channels import Group
from django.conf import settings
import requests

# local imports
from core.celeryapp import app as celery
from core.redisapp import redis
from processing.models import Event
from processing.buckets import DataStoreService


@celery.task
def process_event(event):

	print 'New event for user: %s' % event['user']
	Group("events").send({
		"text": event
	})

	Event.objects.get_or_create(
		user_name=event["user"],
		date=pytz.utc.localize(datetime.utcfromtimestamp(event["date"]/1000)),
		event_type=event["eventType"],
		event_info=event.get("eventInfo", {})
		)

	# update statistics
	DataStoreService().update_buckets(event)

