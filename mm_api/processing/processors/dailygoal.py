from processing.processors.base import BaseProcessor


class DailyGoalProcessor(BaseProcessor):
    processor_for_events = (
      'DailyGoalProgressEvent',
      'DailyGoalCompletedEvent'
    )

    def __init__(self, event):
      super(DailyGoalProcessor, self).__init__()