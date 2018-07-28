# standard library imports
import pytz
from datetime import datetime

# third party imports
from channels import Group

# local imports
from processing.processors.base import BaseProcessor
from processing.models import Event
from processing.buckets import DataStoreService


class DailyGoalProcessor(BaseProcessor):
	processor_for_events = (
		'DailyGoalProgressEvent',
		'DailyGoalCompletedEvent'
	)

	def __init__(self, event=None):
		super(DailyGoalProcessor, self).__init__(event)

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

	def daily_goal_progress_event(self):
		print 'DailyGoalProgressEvent'

	def daily_goal_complete_event(self):
		print 'DailyGoalCompletedEvent'
		# update statistics
		DataStoreService().update_buckets(self.event)