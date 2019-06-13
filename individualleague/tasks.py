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
  #free agencies
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
    print(completedmatches)
    if completedmatches:
      #execute free agencies
      montoupdate=item.droppedpokemon
      droppedpokemon=roster.objects.filter(season=item.season,team=item.coach).get(pokemon=item.droppedpokemon)
      montoupdate.kills=droppedpokemon.kills
      droppedpokemon.kills=0
      montoupdate.deaths=droppedpokemon.deaths
      droppedpokemon.deaths=0
      montoupdate.gp=droppedpokemon.gp
      droppedpokemon.gp=0
      montoupdate.gw=droppedpokemon.gw
      droppedpokemon.gw=0
      montoupdate.differential=droppedpokemon.differential
      droppedpokemon.differential=0
      droppedpokemon.zuser="N"
      droppedpokemon.pokemon=item.addedpokemon
      item.executed=True
      item.save()
      droppedpokemon.save() 
      montoupdate.save()
  #trades
  unexecutedtrades=trading.objects.all().filter(executed=False)
  #check if completed matches
  for item in unexecutedtrades:
    request_league=seasonsetting.objects.get(league=item.season.league)
    league_start=request_league.seasonstart
    elapsed=item.timeadded-league_start
    requestedweek=math.ceil(elapsed.total_seconds()/60/60/24/7)
    completedmatches=True
    for i in range(1,requestedweek+1):
      matchofinterest=schedule.objects.filter(season=item.season).filter(Q(team1=item.coach)|Q(team2=item.coach)).get(week=str(i))
      if matchofinterest.replay=="Link":
        completedmatches=False
    print(completedmatches)
    if completedmatches:
      #execute free agencies
      montoupdate=item.droppedpokemon
      droppedpokemon=roster.objects.filter(season=item.season,team=item.coach).get(pokemon=item.droppedpokemon)
      montoupdate.kills=droppedpokemon.kills
      droppedpokemon.kills=0
      montoupdate.deaths=droppedpokemon.deaths
      droppedpokemon.deaths=0
      montoupdate.gp=droppedpokemon.gp
      droppedpokemon.gp=0
      montoupdate.gw=droppedpokemon.gw
      droppedpokemon.gw=0
      montoupdate.differential=droppedpokemon.differential
      droppedpokemon.differential=0
      droppedpokemon.zuser="N"
      droppedpokemon.pokemon=item.addedpokemon
      item.executed=True
      item.save()
      droppedpokemon.save() 
      montoupdate.save()

