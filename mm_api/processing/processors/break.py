from processing.processors.base import BaseProcessor


class BreakSessionProcessor(BaseProcessor):
    processor_for_events = (
      'BreakSessionStartedEvent',
      'BreakSessionCompletedEvent'
    )

    def __init__(self, event):
      super(BreakSessionProcessor, self).__init__()

