from rest_framework import serializers


class EventsSerializer(serializers.Serializer):

	date = serializers.CharField(max_length=255)
	title = serializers.CharField(max_length=255)
	description = serializers.CharField(max_length=255)
