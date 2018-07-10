from processing.tasks import process_event


class ProcessorMetaclass(type):
    def __new__(mcs, name, bases, dct):
        cls = type.__new__(mcs, name, bases, dct)

        def _task(message, sarg=None):
            cls(message).process()

        cls._task = celery.task(name=name)(_task)
        cls._body = _task
        return cls

class BaseProcessor(object):
  __metaclass__ = ProcessorMetaclass

	def __init__(self, event):
		self.event = json.loads(event)

  def process_if(self):
    return self.event["eventType"] in self.processor_for_events

	def process_message(self, event):
		print 'Received event: %s' % event

		process_event.delay(event)

  def process(self):
    method_name = self._method_name_convert(self.message.event_type)
    method = getattr(self, method_name, None)
    if method is not None:
        method()

    self.after_process()


