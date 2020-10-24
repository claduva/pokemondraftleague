from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import UserSerializer, ScheduleSerializer

from individualleague.models import schedule 

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScheduleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = schedule.objects.all()[0:10]
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]