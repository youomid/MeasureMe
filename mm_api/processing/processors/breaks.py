# standard library imports
import pytz
from datetime import datetime


from processing.processors.base import BaseProcessor
from channels import Group
from processing.models import Event
from processing.buckets import DataStoreService


class BreakSessionProcessor(BaseProcessor):
	processor_for_events = (
		'BreakSessionStartedEvent',
		'BreakSessionCompletedEvent'
	)

	def __init__(self, event=None):
		super(BreakSessionProcessor, self).__init__(event)
		
	def before_process(self):
		# send events to channels group to be sent to the events feed
		Group("events").send({
			"text": self.event
		})

		Event.objects.get_or_create(
			user_name=self.event["user"],
			date=pytz.utc.localize(datetime.utcfromtimestamp(self.event["date"]/1000)),
			event_type=self.event["eventType"],
			event_info=self.event.get("eventInfo", {}),
			)

	def break_session_started_event(self):
		print 'BreakSessionStartedEvent'

	def break_session_completed_event(self):
		print 'BreakSessionCompletedEvent'
		# update statistics
		DataStoreService().update_buckets(self.event)

