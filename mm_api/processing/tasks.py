# standard library imports
import ast
import json
import time
import pytz
import requests
from datetime import datetime

# third party imports
from channels import Group
from django.conf import settings

# local imports
from core.celeryapp import app as celery
from core.redisapp import redis
from processing.models import Event
from processing.buckets import DataStoreService


@celery.task
def process_event(event):
	"""
	Process event by sending events to the realtime event feed, storing events
	in postgres and updating the buckets in redis.

		Args:	
			event: a dictionary containing event information

		Return:
			None

	"""

	# send events to channels group to be sent to the events feed
	Group("events").send({
		"text": event
	})

	Event.objects.get_or_create(
		user_name=event["user"],
		date=pytz.utc.localize(datetime.utcfromtimestamp(event["date"]/1000)),
		event_type=event["eventType"],
		event_info=event.get("eventInfo", {}),
		)

	# update statistics
	DataStoreService().update_buckets(event)

