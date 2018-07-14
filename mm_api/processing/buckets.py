from processing.redis_models import RedisDictModel
from datetime import datetime

class Bucket(RedisDictModel):
	default = {
		'comp_ws': 0,
		'incomp_ws': 0,
		'pws': 0,
		'daily_c': 0,
		'comp_bs': 0,
	}

	def __init__(self, redis_id):
		super(Bucket, self).__init__(redis_id)


class HourlyBucket(Bucket):
	def __init__(self, redis_id):
		super(HourlyBucket, self).__init__(redis_id)


class DataStoreService(object):

	bucket_types = [
		HourlyBucket
	]

	def get_times(self, time):
		"""
		Use the event time to get the start and end of the hour.
		"""

		dt = datetime.utcfromtimestamp(time/1000.0)
		# round down to nearest hour
		dt = dt.replace(minute=0,second=0,microsecond=0)

		# convert to milliseconds
		start_time = (dt - datetime.utcfromtimestamp(0)).total_seconds() * 1000

		dt = dt.replace(minute=59,second=59,microsecond=999999)

		end_time = (dt - datetime.utcfromtimestamp(0)).total_seconds() * 1000

		return start_time, end_time

	def generate_bucket_name(self, event):
		"""
		Create a unique id that is used for redis keys.

		Return:
			Example: "HourlyBucket:guest|1531584000000|1531587599999"

		"""
		start_time, end_time = self.get_times(event.get("date"))
		return "%s|%d|%d" % (event.get("user"), start_time, end_time)

	def update_buckets(self, event):
		for bucket_type in self.bucket_types:
			bucket = bucket_type(self.generate_bucket_name(event))
			self.update_stats(bucket, event)

	def update_stats(self, bucket, event):
		"""
		Update the appropriate metrics based on the event type.
		"""

		if event.get("eventType") == "WorkSessionCompletedEvent":
			bucket.increment('comp_ws', 1)
		elif event.get("eventType") == "WorkSessionPausedEvent":
			bucket.increment('pws', 1)
		elif event.get("eventType") == "WorkSessionResetEvent":
			bucket.increment('incomp_ws', 1)
		elif event.get("eventType") == "BreakSessionCompletedEvent":
			bucket.increment('comp_bs', 1)
		elif event.get("eventType") == "DailyGoalCompletedEvent":
			bucket.increment('daily_c', 1)














