# standard library imports
import pytz
from datetime import datetime

# third party imports
from channels import Group

# local imports
from processing.processors.base import BaseProcessor
from processing.models import Event
from processing.buckets import DataStoreService

class WorkSessionProcessor(BaseProcessor):
	processor_for_events = (
		'WorkSessionStartedEvent',
		'WorkSessionPausedEvent',
		'WorkSessionRestartedEvent',
		'WorkSessionCompletedEvent'
	)

	def __init__(self, event=None):
		super(WorkSessionProcessor, self).__init__(event)
		
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

	def work_session_started_event(self):
		print 'WorkSessionStartedEvent'

	def work_session_paused_event(self):
		print 'WorkSessionPausedEvent'
		# update statistics
		DataStoreService().update_buckets(self.event)

	def work_session_restarted_event(self):
		print 'WorkSessionRestartedEvent'
		# update statistics
		DataStoreService().update_buckets(self.event)
		
	def work_session_completed_event(self):
		print 'WorkSessionCompletedEvent'
		# update statistics
		DataStoreService().update_buckets(self.event)
