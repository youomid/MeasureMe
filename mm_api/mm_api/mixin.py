
from collections import defaultdict




class BucketsMixin(object):

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
			temp_dict = period.default
			temp_dict['start_time'] = period.start_time
			temp_dict['end_time'] = period.end_time
			dict_buckets.append(temp_dict)

		return dict_buckets






