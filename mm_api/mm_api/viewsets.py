from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django.conf import settings

import requests


class SimulationViewSet(viewsets.ViewSet):
	"""
	Send requests to the event source server to simulate work scenarios.
	"""
	
	url = settings.EVENTS_SOURCE_URL	

	@list_route(methods=['GET'])
	def complete_work_session(self, request):
		requests.post(url=self.url, data="complete-work-session")
		return Response("Success", status=200)

	@list_route(methods=['GET'])
	def incomplete_work_session(self, request):
		requests.post(url=self.url, data="incomplete-work-session")
		return Response("Success", status=200)

	@list_route(methods=['GET'])
	def paused_work_session(self, request):
		requests.post(url=self.url, data="paused-work-session")
		return Response("Success", status=200)

	@list_route(methods=['GET'])
	def daily_complete(self, request):
		requests.post(url=self.url, data="daily-goal-complete")
		return Response("Success", status=200)