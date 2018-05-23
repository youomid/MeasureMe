from rest_framework.generics import GenericAPIView
from django.http import HttpResponse


class SummaryView(GenericAPIView):

	def get(self, request, *args, **kwargs):
		return HttpResponse("SummaryView")