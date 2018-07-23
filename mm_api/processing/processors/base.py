from core.celeryapp import app as celery
from processing.tasks import process_event
import json
import re


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

class ProcessorMetaclass(type):
	def __new__(mcs, name, bases, dct):
		cls = type.__new__(mcs, name, bases, dct)

		def _task(message, sarg=None):
			cls(message).process()

		if not dct.get('_no_task') is True:
			cls._task = celery.task(name=name)(_task)
		return cls

class BaseProcessor(object):
	__metaclass__ = ProcessorMetaclass
	_no_task = True

	def __init__(self, event=None):
		if type(event) == dict:
			self.event = event
		elif event:
			self.event = json.loads(event)

	def process_if(self):
		return self.event["eventType"] in self.processor_for_events

	def process_message(self):
		self._task.delay(self.event, None)

	@staticmethod
	def _method_name_convert(name):
		"""
		Converts event name to its respective method name.
		"""

		s1 = first_cap_re.sub(r'\1_\2', name)
		return all_cap_re.sub(r'\1_\2', s1).lower()

	def process(self):

		self.before_process()

		method_name = self._method_name_convert(self.event['eventType'])
		method = getattr(self, method_name, None)
		if method is not None:
			method()

