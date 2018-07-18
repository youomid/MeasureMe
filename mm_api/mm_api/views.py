from rest_framework.generics import GenericAPIView
from django.http import HttpResponse
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
from django.core.serializers.json import DjangoJSONEncoder



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


class DashboardView(GenericAPIView):
	serializer_class = DashboardSerializer
	
	def get(self, request, *args, **kwargs):
		return HttpResponse({
				'events': self.get_events(),
				'daily_history': self.get_daily_history(),
				'monthly_history': self.get_monthly_history()
			})

	def get_events(self):
		last_day = datetime.now() - timedelta(days=1)
		# get events from the last day
		events = (Event.objects.filter(date__gte=last_day)
			.values('date', 'event_type'))
		return json.dumps(list(events), cls=DjangoJSONEncoder)

	def get_daily_history(self):
		
		pass

	def get_monthly_history(self):
		
		pass
		






