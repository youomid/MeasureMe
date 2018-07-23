from rest_framework.generics import GenericAPIView
from django.http import HttpResponse
from rest_framework.response import Response
from django.conf import settings
import redis
import json
from channels import Group
from datetime import datetime, timedelta

from .serializers import (
	EventsSerializer,
	DashboardSerializer
	)

from processing.models import Event
from core.redisapp import redis
from processing.buckets import DataStoreService

from .mixin import BucketsMixin


class DashboardView(GenericAPIView, BucketsMixin):
	"""
	Retrieve the monthly history, daily history and events feed for the dashboard.
	"""

	metrics = [
		'comp_ws', 'incomp_ws', 'pws', 'daily_c',
		'comp_bs', 'earned_bp', 'consumed_bp'
		]
	
	def get(self, request, *args, **kwargs):
		user_name = request.user.get_username()
		return Response({
				'events': self.get_events(user_name),
				'daily_history': self.get_daily_history(user_name),
				'monthly_history': self.get_monthly_history(user_name)
			})

	def get_events(self, user):
		"""
		Retrieve events from the last day.
		"""
		last_day = datetime.now() - timedelta(days=1)
		events = (Event.objects.filter(user_name=user,date__gte=last_day)
			.values('date', 'event_type', 'description'))

		def str_time(event):
			event['date'] = event['date'].strftime('%m/%d/%Y %H:%M:%S')
			return event

		return map(str_time, events)

	def get_daily_history(self, user):
		buckets = DataStoreService().get_buckets_current_day(user)
		return self.convert_buckets_to_dict(buckets)

	def get_monthly_history(self, user):
		buckets = DataStoreService().get_buckets_current_month(user)	
		return self.generate_bucket_lists(buckets)






