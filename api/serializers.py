from django.contrib.auth.models import User
from rest_framework import serializers

from individualleague.models import schedule
from leagues.models import coachdata

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = coachdata
        fields = [
                'teamname'
            ]

class ScheduleSerializer(serializers.ModelSerializer):
    team1name = serializers.CharField(read_only=True, source="team1.teamname")
    team2name = serializers.CharField(read_only=True, source="team2.teamname")
    discordserver = serializers.CharField(read_only=True, source="season.subleague.discord_settings.discordserver")
    discordchannel = serializers.CharField(read_only=True, source="season.subleague.discord_settings.replaychannel")

    class Meta:
        model = schedule
        fields = [
            'week',
            'team1name',
            'team2name',
            'replay', 
            'discordserver',
            'discordchannel'
            ]

