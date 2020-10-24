from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import ScheduleSerializer, OverdueSerializer

from datetime import datetime, timedelta

from individualleague.models import schedule 

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = schedule.objects.filter(announced=False).exclude(replay="Link")
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.AllowAny]

class OverdueViewSet(viewsets.ModelViewSet):
    queryset = schedule.objects.filter(replay="Link").filter(duedate__lt=datetime.now())
    serializer_class = OverdueSerializer
    permission_classes = [permissions.AllowAny]