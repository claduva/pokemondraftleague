from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import ScheduleSerializer, OverdueSerializer, DraftAnnouncementSerializer

from datetime import datetime, timedelta

from individualleague.models import schedule 
from leagues.models import draft

class OverdueViewSet(viewsets.ModelViewSet):
    queryset = schedule.objects.filter(replay="Link").filter(duedate__lt=datetime.now()).order_by('duedate')
    serializer_class = OverdueSerializer
    permission_classes = [permissions.AllowAny]

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = schedule.objects.filter(announced=False).exclude(replay="Link")
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.AllowAny]

class DraftAnnouncementViewSet(viewsets.ModelViewSet):
    queryset = draft.objects.all().filter(announced=False).exclude(pokemon__isnull=True).order_by('picknumber')
    serializer_class = DraftAnnouncementSerializer
    permission_classes = [permissions.AllowAny]
