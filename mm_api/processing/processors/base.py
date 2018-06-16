


class BaseProcessor(object):

	def __init__(self):
		pass

	def process_message(self, event):
		print 'Received event: %s' % event

		

