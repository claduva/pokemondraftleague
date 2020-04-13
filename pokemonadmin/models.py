from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage
from django.contrib.postgres.fields import JSONField, ArrayField
import urllib
import os
from enum import Enum

from leagues.models import *
from individualleague.models import schedule

class historical_team(models.Model):
    league = models.ForeignKey(league, on_delete=models.CASCADE)
    seasonname = models.CharField(max_length=100)
    subseason = models.CharField(max_length=100, null=True)
    teamname = models.CharField(max_length=100)
    subteam = models.CharField(max_length=100, null=True)
    coach1= models.ForeignKey(User, on_delete=models.CASCADE,related_name="historical_team_coach1")
    coach1username=models.CharField(max_length=100)
    coach2=models.ForeignKey(User, on_delete=models.CASCADE,related_name="historical_team_coach2",null=True)
    coach2username=models.CharField(max_length=100,null=True)
    logo = models.ImageField(default='league_logos/defaultleaguelogo.png',upload_to='historic_league_logos',null=True, blank=True)
    logo_url=models.URLField(default="")
    wins=models.IntegerField(default=0)
    losses=models.IntegerField(default=0)
    differential=models.IntegerField(default=0)
    forfeit=models.IntegerField(default=0)
    support = models.IntegerField(default=0)
    damagedone = models.IntegerField(default=0)
    hphealed = models.IntegerField(default=0)
    luck = models.FloatField(default=0)
    remaininghealth = models.IntegerField(default=0)

    class Meta:
        ordering = ['-seasonname','teamname']

    def __str__(self):
        return f'{self.league.name} ({self.subseason}): {self.seasonname} {self.teamname}'

class historical_draft(models.Model):
    team = models.ForeignKey(historical_team, on_delete=models.CASCADE,related_name="historical_draft")
    pokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True,related_name="historicalpokemondraft")
    picknumber = models.IntegerField(default=0)

    class Meta:
        ordering = ['picknumber']

class historical_roster(models.Model):
    team = models.ForeignKey(historical_team, on_delete=models.CASCADE,related_name="historical_roster")
    pokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True,related_name="historicalpokemonroster")
    kills = models.IntegerField(default=0)
    deaths =  models.IntegerField(default=0)
    differential = models.IntegerField(default=0)
    gp = models.IntegerField(default=0)
    gw = models.IntegerField(default=0)
    support = models.IntegerField(default=0)
    damagedone = models.IntegerField(default=0)
    hphealed = models.IntegerField(default=0)
    luck = models.FloatField(default=0)
    remaininghealth = models.IntegerField(default=0)

    class Meta:
        ordering = ['pokemon__pokemon']

class historical_freeagency(models.Model):
    team = models.ForeignKey(historical_team, on_delete=models.CASCADE,related_name="historical_freeagency")
    addedpokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True,related_name="addfa")
    droppedpokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True,related_name="dropfa")

class historical_trading(models.Model):
    team = models.ForeignKey(historical_team, on_delete=models.CASCADE)
    addedpokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True,related_name="addtrade")
    droppedpokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True,related_name="droptrade") 

class historical_match(models.Model):
    week=models.CharField(max_length=30)
    team1=models.ForeignKey(historical_team, on_delete=models.CASCADE,related_name='historict1')
    team1alternateattribution=models.ForeignKey(User,on_delete=models.CASCADE, related_name="historicteam1alternateattribution",null=True)
    team2=models.ForeignKey(historical_team, on_delete=models.CASCADE,related_name='historict2')
    team2alternateattribution=models.ForeignKey(User,on_delete=models.CASCADE, related_name="historicteam2alternateattribution",null=True)
    winner = models.ForeignKey(historical_team, on_delete=models.CASCADE,null=True,related_name='historicwinner')
    winneralternateattribution=models.ForeignKey(User,on_delete=models.CASCADE, related_name="historicwinneralternateattribution",null=True)
    team1score = models.IntegerField(default=0)
    team2score = models.IntegerField(default=0)
    replay = models.CharField(max_length=100,default="Link")
    team1usedz = models.BooleanField(default=False)
    team2usedz = models.BooleanField(default=False)
    team1megaevolved = models.BooleanField(default=False)
    team2megaevolved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.team1.league.name} {self.team1.seasonname} Week {self.week} {self.team1.teamname} vs. {self.team2.teamname}'


class historical_match_replay(models.Model):
    match=models.OneToOneField(historical_match,on_delete=models.CASCADE)
    data=JSONField()

class error_message(models.Model):
    associated_view=models.CharField(max_length=200)
    error_message=models.CharField(max_length=200)

class replaydatabase(models.Model):
    associatedmatch=models.OneToOneField(schedule,on_delete=models.CASCADE,null=True)
    associatedhistoricmatch=models.OneToOneField(historical_match,on_delete=models.CASCADE,null=True)
    team1coach1=models.ForeignKey(User,on_delete=models.CASCADE,related_name="team1coach1")
    team1coach2=models.ForeignKey(User,on_delete=models.CASCADE,related_name="team1coach2",null=True)
    team2coach1=models.ForeignKey(User,on_delete=models.CASCADE,related_name="team2coach1")
    team2coach2=models.ForeignKey(User,on_delete=models.CASCADE,related_name="team2coach2",null=True)
    winnercoach1=models.ForeignKey(User,on_delete=models.CASCADE,related_name="winnercoach1",null=True)
    winnercoach2=models.ForeignKey(User,on_delete=models.CASCADE,related_name="winnercoach2",null=True)
    replayuser1=models.CharField(max_length=200)
    replayuser2=models.CharField(max_length=200)
    winneruser=models.CharField(max_length=200,default="")
    replay=models.CharField(max_length=500)

class favoritereplay(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_favorities')
    replay=models.ForeignKey(replaydatabase,on_delete=models.CASCADE,related_name='users_favorited')

class historic_manual_replay(models.Model):
    match=models.OneToOneField(historical_match,on_delete=models.CASCADE)
    t1pokemon1=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='HistTeam1Pokemon1')
    t1pokemon2=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='HistTeam1Pokemon2')
    t1pokemon3=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='HistTeam1Pokemon3')
    t1pokemon4=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='HistTeam1Pokemon4')
    t1pokemon5=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='HistTeam1Pokemon5')
    t1pokemon6=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='HistTeam1Pokemon6')
    t2pokemon1=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='HistTeam2Pokemon1')
    t2pokemon2=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='HistTeam2Pokemon2')
    t2pokemon3=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='HistTeam2Pokemon3')
    t2pokemon4=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='HistTeam2Pokemon4')
    t2pokemon5=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='HistTeam2Pokemon5')
    t2pokemon6=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='HistTeam2Pokemon6')
    t1pokemon1kills=models.IntegerField(default=0)
    t1pokemon2kills=models.IntegerField(default=0)
    t1pokemon2kills=models.IntegerField(default=0)
    t1pokemon3kills=models.IntegerField(default=0)
    t1pokemon4kills=models.IntegerField(default=0)
    t1pokemon5kills=models.IntegerField(default=0)
    t1pokemon6kills=models.IntegerField(default=0)
    t2pokemon1kills=models.IntegerField(default=0)
    t2pokemon2kills=models.IntegerField(default=0)
    t2pokemon3kills=models.IntegerField(default=0)
    t2pokemon4kills=models.IntegerField(default=0)
    t2pokemon5kills=models.IntegerField(default=0)
    t2pokemon6kills=models.IntegerField(default=0)
    t1pokemon1death=models.IntegerField(default=0)
    t1pokemon2death=models.IntegerField(default=0)
    t1pokemon3death=models.IntegerField(default=0)
    t1pokemon4death=models.IntegerField(default=0)
    t1pokemon5death=models.IntegerField(default=0)
    t1pokemon6death=models.IntegerField(default=0)
    t2pokemon1death=models.IntegerField(default=0)
    t2pokemon2death=models.IntegerField(default=0)
    t2pokemon3death=models.IntegerField(default=0)
    t2pokemon4death=models.IntegerField(default=0)
    t2pokemon5death=models.IntegerField(default=0)
    t2pokemon6death=models.IntegerField(default=0)