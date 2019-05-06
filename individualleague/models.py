from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage

from leagues.models import *

class schedule(models.Model):
    season = models.ForeignKey(seasonsetting,on_delete=models.CASCADE)
    week=models.IntegerField()
    team1 = models.ForeignKey(coachdata,on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(coachdata,on_delete=models.CASCADE, related_name="team2")
    winner = models.ForeignKey(coachdata,on_delete=models.CASCADE, related_name="winner",null=True)
    team1score = models.IntegerField(default=0)
    team2score = models.IntegerField(default=0)
    replay = models.CharField(max_length=100)
    team1usedz = models.BooleanField(default=False)
    team2usedz = models.BooleanField(default=False)
    team1megaevolved = models.BooleanField(default=False)
    team2megaevolved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.season.league.name} Week {self.week} match between {self.team1.teamabbreviation} vs. {self.team1.teamabbreviation}'

