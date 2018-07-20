
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




