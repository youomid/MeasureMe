from django.core.management.base import BaseCommand
from django.conf import settings

from processing.stream import EventStream


class Command(BaseCommand):
    args = ''
    help = 'Fetch event messages from RMQ to distribute to celery workers'

    def handle(self, *args, **options):
        self.handle_event_channel()

    @staticmethod
    def handle_event_channel():
    	event_stream = EventStream()
    	event_stream.start()
