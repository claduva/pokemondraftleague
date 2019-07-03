from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage
from PIL import Image
from enum import Enum

from leagues.models import *

class schedule(models.Model):
    season = models.ForeignKey(seasonsetting,on_delete=models.CASCADE,related_name="schedule")
    week=models.CharField(max_length=30)
    team1 = models.ForeignKey(coachdata,on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(coachdata,on_delete=models.CASCADE, related_name="team2")
    winner = models.ForeignKey(coachdata,on_delete=models.CASCADE, related_name="winner",null=True)
    team1score = models.IntegerField(default=0)
    team2score = models.IntegerField(default=0)
    replay = models.CharField(max_length=100,default="Link")
    team1usedz = models.BooleanField(default=False)
    team2usedz = models.BooleanField(default=False)
    team1megaevolved = models.BooleanField(default=False)
    team2megaevolved = models.BooleanField(default=False)
    timestamp= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.season.league.name} Week {self.week} match between {self.team1.teamabbreviation} vs. {self.team1.teamabbreviation}'

class playoff_match(models.Model):
    season = models.ForeignKey(seasonsetting,on_delete=models.CASCADE)
    playoffround=models.CharField(max_length=15)
    team1 = models.ForeignKey(coachdata,on_delete=models.CASCADE, related_name="playoffteam1")
    team2 = models.ForeignKey(coachdata,on_delete=models.CASCADE, related_name="playoffteam2")
    winner = models.ForeignKey(coachdata,on_delete=models.CASCADE, related_name="playoffwinner",null=True)
    team1score = models.IntegerField(default=0)
    team2score = models.IntegerField(default=0)
    replay = models.CharField(max_length=100,default="Link")
    team1usedz = models.BooleanField(default=False)
    team2usedz = models.BooleanField(default=False)
    team1megaevolved = models.BooleanField(default=False)
    team2megaevolved = models.BooleanField(default=False)
    timestamp= models.DateTimeField(auto_now=True)

class rule(models.Model):
    season = models.ForeignKey(seasonsetting,on_delete=models.CASCADE)
    rules=models.TextField(default="No rules announced")

    def __str__(self):
        return f'Rules for {self.season.league.name}'

class free_agency(models.Model):
    coach=models.ForeignKey(coachdata,on_delete=models.CASCADE)
    season=models.ForeignKey(seasonsetting,on_delete=models.CASCADE)
    droppedpokemon=models.ForeignKey(all_pokemon,on_delete=models.CASCADE,related_name="dropped")
    addedpokemon=models.ForeignKey(all_pokemon,on_delete=models.CASCADE,related_name="added")
    timeadded=models.DateTimeField(auto_now_add=True)
    executed=models.BooleanField(default=False)
    
class trade_request(models.Model):
    offeredpokemon=models.ForeignKey(roster,on_delete=models.CASCADE,related_name="tradedroppedrequest")
    requestedpokemon=models.ForeignKey(roster,on_delete=models.CASCADE,related_name="tradeaddedrequest")

class trading(models.Model):
    coach=models.ForeignKey(coachdata,on_delete=models.CASCADE)
    season=models.ForeignKey(seasonsetting,on_delete=models.CASCADE)
    droppedpokemon=models.ForeignKey(all_pokemon,on_delete=models.CASCADE,related_name="tradedropped")
    addedpokemon=models.ForeignKey(all_pokemon,on_delete=models.CASCADE,related_name="tradeadded")
    timeadded=models.DateTimeField(auto_now_add=True)
    executed=models.BooleanField(default=False)

class hall_of_fame_entry(models.Model):
    league=models.ForeignKey(league,on_delete=models.CASCADE)
    seasonname=models.CharField(max_length=30,default="Not Specified")
    championteamname=models.CharField(max_length=50,default="Not Specified")
    championcoachname=models.CharField(max_length=50,default="Not Specified")
    champlogo = models.ImageField(upload_to='champlogos',null=True, blank=True)
    runnerupteamname=models.CharField(max_length=50,default="Not Specified")
    runnerupcoachname=models.CharField(max_length=50,default="Not Specified")
    championshipreplay=models.CharField(max_length=100,default="Not Specified")

class hall_of_fame_roster(models.Model):
    hall_of_frame_entry=models.ForeignKey(hall_of_fame_entry,on_delete=models.CASCADE,related_name="hofentries")
    pokemon=models.ForeignKey(all_pokemon,on_delete=models.CASCADE)

    class Meta:
        ordering = ['pokemon__pokemon']

class left_pick(models.Model):
    coach=models.ForeignKey(coachdata,on_delete=models.CASCADE)
    season=models.ForeignKey(seasonsetting,on_delete=models.CASCADE)
    pick=models.ForeignKey(all_pokemon,on_delete=models.CASCADE,related_name="leftpick")
    backup=models.ForeignKey(all_pokemon,on_delete=models.CASCADE,related_name="backuppick")

class replay_announcements(models.Model):
    league = models.CharField(max_length=100)
    league_name = models.CharField(max_length=1000)
    text = models.CharField(max_length=1000)
    replaychannel = models.CharField(max_length=100,null=True)

class freeagency_announcements(models.Model):
    league = models.CharField(max_length=100)
    league_name = models.CharField(max_length=1000)
    text = models.CharField(max_length=1000)
    freeagencychannel = models.CharField(max_length=100,null=True)
    
class trading_announcements(models.Model):
    league = models.CharField(max_length=100)
    league_name = models.CharField(max_length=1000)
    text = models.CharField(max_length=1000)
    tradingchannel = models.CharField(max_length=100,null=True)