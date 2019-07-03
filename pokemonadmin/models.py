from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage

from enum import Enum

from leagues.models import *

class historical_team(models.Model):
    league = models.ForeignKey(league, on_delete=models.CASCADE)
    seasonname = models.CharField(max_length=100)
    teamname = models.CharField(max_length=100)
    coach1= models.ForeignKey(User, on_delete=models.CASCADE,related_name="historical_team_coach1")
    coach2=models.ForeignKey(User, on_delete=models.CASCADE,related_name="historical_team_coach2")
    logo = models.ImageField(default='league_logos/defaultleaguelogo.png',upload_to='historic_league_logos',null=True, blank=True)

class historical_draft(models.Model):
    team = models.ForeignKey(historical_team, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True,related_name="historicalpokemondraft")

    class Meta:
        ordering = ['id']

class historical_roster(models.Model):
    team = models.ForeignKey(historical_team, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True,related_name="historicalpokemonroster")
    kills = models.IntegerField(default=0)
    deaths =  models.IntegerField(default=0)
    differential = models.IntegerField(default=0)
    gp = models.IntegerField(default=0)
    gw = models.IntegerField(default=0)

class historical_freeagency(models.Model):
    team = models.ForeignKey(historical_team, on_delete=models.CASCADE)
    addedpokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True,related_name="addfa")
    droppededpokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True,related_name="dropfa")

class historical_trading(models.Model):
    team = models.ForeignKey(historical_team, on_delete=models.CASCADE)
    addedpokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True,related_name="addtrade")
    droppededpokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True,related_name="droptrade") 

class historical_match(models.Model):
    week=models.CharField(max_length=30)
    team1=models.ForeignKey(historical_team, on_delete=models.CASCADE,related_name='historict1')
    team2=models.ForeignKey(historical_team, on_delete=models.CASCADE,related_name='historict2')
    winner = models.ForeignKey(historical_team, on_delete=models.CASCADE,null=True,related_name='historicwinner')
    team1score = models.IntegerField(default=0)
    team2score = models.IntegerField(default=0)
    replay = models.CharField(max_length=100,default="Link")
    team1usedz = models.BooleanField(default=False)
    team2usedz = models.BooleanField(default=False)
    team1megaevolved = models.BooleanField(default=False)
    team2megaevolved = models.BooleanField(default=False)