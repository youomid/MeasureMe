from rest_framework.generics import GenericAPIView
from django.http import HttpResponse
from django.conf import settings
import redis


class SummaryView(GenericAPIView):

	def get(self, request, *args, **kwargs):
		r = redis.StrictRedis(host=settings.REDIS_DATASTORE['host'],
			port=settings.REDIS_DATASTORE['port'],
			db=settings.REDIS_DATASTORE['db'])

		return HttpResponse(r.get("test"))