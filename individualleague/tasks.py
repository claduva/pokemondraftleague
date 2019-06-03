from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime, timedelta,timezone
import math
from django.db.models import Q

from pokemondraftleague.celery import app

from .models import free_agency
from leagues.models import seasonsetting
from individualleague.models import schedule, roster

@shared_task(name = "print_msg_test")
def print_message_test():
  print("Celery is working!!")

@shared_task(name = "execute_fa_and_trades")
def execute_free_agency_and_trades():
  unexecutedfa=free_agency.objects.all().filter(executed=False)
  #check if completed matches
  for item in unexecutedfa:
    request_league=seasonsetting.objects.get(league=item.season.league)
    league_start=request_league.seasonstart
    elapsed=item.timeadded-league_start
    requestedweek=math.ceil(elapsed.total_seconds()/60/60/24/7)
    completedmatches=True
    for i in range(1,requestedweek+1):
      matchofinterest=schedule.objects.filter(season=item.season).filter(Q(team1=item.coach)|Q(team2=item.coach)).get(week=str(i))
      if matchofinterest.replay=="Link":
        completedmatches=False
  if completedmatches:
    #execute free agencies
    item.executed=True
    item.save()
    print("saved")
    #droppedpokemon=roster.objects.filter(season=season,team=coach).get(pokemon=form.cleaned_data['droppedpokemon'])
    #droppedpokemon.kills=0
    #droppedpokemon.deaths=0
    #droppedpokemon.gp=0
    #droppedpokemon.gw=0
    #droppedpokemon.differential=0
    #droppedpokemon.zuser="N"
    #droppedpokemon.pokemon=form.cleaned_data['addedpokemonBBB']
    #droppedpokemon.save() 

