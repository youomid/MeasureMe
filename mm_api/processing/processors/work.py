from processing.processors.base import BaseProcessor


class WorkSessionProcessor(BaseProcessor):
  processor_for_events = (
      'WorkSessionStartedEvent',
      'WorkSessionPausedEvent',
      'WorkSessionRestartedEvent',
      'WorkSessionCompletedEvent'
    )

    def __init__(self, event):
      super(WorkSessionProcessor, self).__init__()