# standard library imports
import ast
import json
import time
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

  event_dict = json.loads(event)

	Group("events").send({
		"text": event
	})

  Event.objects.get_or_create(
    user_name=event_dict["user"],
    date=datetime.utcfromtimestamp(event_dict["date"]),
    event_type=event_dict["eventType"],
    event_info=event_dict["eventInfo"]
    )

  # TODO: Process data and store in redis buckets
  

