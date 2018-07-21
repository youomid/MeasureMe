
from collections import defaultdict
import random
from datetime import datetime



class BucketsMixin(object):

	def convert_ms_to_str(self, time_ms):
		"""
		Convert milliseconds to string format.
		"""

		return datetime.fromtimestamp(time_ms/1000.0).strftime('%m/%d/%Y %H:%M:%S')

	def aggregate_buckets(self, buckets):
		"""
		Aggregate bucket data into a single dictionary. 
		"""

		aggregated_data = defaultdict(int)

		for bucket in buckets:
			for metric in self.metrics:
				aggregated_data[metric] += bucket[metric]

		return aggregated_data

	def convert_buckets_to_dict(self, buckets):
		"""
		Convert bucket objects to dictionary and include their start and end time.
		"""

		dict_buckets = []

		for period in buckets:
			temp_dict = period.default.copy()
			temp_dict['start_time'] = self.convert_ms_to_str(period.start_time)
			temp_dict['end_time'] = self.convert_ms_to_str(period.end_time)
			dict_buckets.append(temp_dict)

		return dict_buckets

	def generate_bucket_lists(self, buckets):
		"""
		Create lists from bucket objects to be used by the dashboard monthly history chart.
		"""

		final_data = defaultdict(list)

		for period in buckets:
			final_data['start_time'].append(self.convert_ms_to_str(period.start_time))
			# create dict entry with a list of the metric values
			for metric in self.metrics:
				final_data[metric].append(period[metric] + random.randint(1,10))

		return final_data



