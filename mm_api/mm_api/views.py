from rest_framework.generics import GenericAPIView
from django.http import HttpResponse
from django.conf import settings
import redis
import json
from channels import Group

from .serializers import (
	EventsSerializer
	)

from processing.models import Event


class SummaryView(GenericAPIView):

	def get(self, request, *args, **kwargs):
		# r = redis.StrictRedis(
		# 	host=settings.REDIS_DATASTORE['host'],
		# 	port=settings.REDIS_DATASTORE['port'],
		# 	db=settings.REDIS_DATASTORE['db']
		# )

		# return HttpResponse(r.get("test"))
		Group("events").send({
	        "text": "Message from summary view",
	    })

		return HttpResponse("SummaryView")


class EventsView(GenericAPIView):
	serializer_class = EventsSerializer

	def get(self, request, *args, **kwargs):

		return Response(serializer_class(
			Event.objects.filter(request.GET.get('username')),
			many=True)
		)

	def post(self, request, *args, **kwargs):
		Group("events").send({
	        "text": json.dumps(request.data),
	    })

		return HttpResponse("Event has been stored.")