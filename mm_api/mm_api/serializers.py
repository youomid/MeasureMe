# standard library imports

# third party imports
from rest_framework import serializers

# local imports


class EventsSerializer(serializers.Serializer):
	description = serializers.CharField(max_length=255)
	title = serializers.CharField(max_length=255)
	date = serializers.DateTimeField()


class DashboardSerializer(serializers.Serializer):
	date = serializers.DateTimeField()
	event_type = serializers.CharField(max_length=255)
