from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField


class Event(models.Model):
	user_name = models.CharField(max_length=30)
	date = models.DateTimeField(auto_now_add=True, blank=True) 
	event_type = models.CharField(max_length=50)
	event_info = JSONField()
	description = models.CharField(max_length=255, default="No description.")
	