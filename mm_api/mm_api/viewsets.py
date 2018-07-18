from rest_framework import viewsets
from rest_framework.response import Response



class SimulationViewSet(viewsets.ViewSet):
  
  def complete_work_session(self, request):
    print "complete_work_session"


  def incomplete_work_session(self, request):
    print "incomplete_work_session"


  def paused_work_session(self, request):
    print "paused_work_session"


  def daily_complete(self, request):
    print "daily_complete"