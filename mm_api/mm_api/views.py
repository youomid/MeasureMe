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



class SummaryView(GenericAPIView):

	def get(self, request, *args, **kwargs):

		Group("events").send({
	        "text": "Message from summary view",
	    })

		return HttpResponse("SummaryView")


class EventsView(GenericAPIView):
	serializer_class = EventsSerializer

	def get(self, request, *args, **kwargs):

		return HttpResponse(self.serializer_class(
			Event.objects.filter(request.GET.get('username')),
			many=True)
		)

	def post(self, request, *args, **kwargs):
		Group("events").send({
	        "text": json.dumps(request.data),
	    })

		return HttpResponse("Event has been stored.")


class DashboardView(GenericAPIView, BucketsMixin):
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
		last_day = datetime.now() - timedelta(days=1)
		# get events from the last day
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






