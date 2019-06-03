from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime, timedelta,timezone
import pytz

from pokemondraftleague.celery import app

from .models import free_agency
from leagues.models import seasonsetting

@shared_task(name = "print_msg_test")
def print_message_test():
  print("Celery is working!!")


@shared_task(name = "execute_fa_and_trades")
def execute_free_agency_and_trades():
  #get unexecuted free agency requests
  unexecutedfa=free_agency.objects.all().filter(executed=False)
  #process unexecuted free agencies
  for item in unexecutedfa:
    #get league start date
    request_league=seasonsetting.objects.get(league=item.season.league)
    league_start=request_league.seasonstart
    timezone = pytz.timezone('UTC')
    elapsed=timezone.localize(item.timeadded)-timezone.localize(league_start)
    week=math.ceil(elapsed.total_seconds()/60/60/24/7)
    #print(str(week))
   


#droppedpokemon=roster.objects.filter(season=season,team=coach).get(pokemon=form.cleaned_data['droppedpokemon'])
#droppedpokemon.kills=0
#droppedpokemon.deaths=0
#droppedpokemon.gp=0
#droppedpokemon.gw=0
#droppedpokemon.differential=0
#droppedpokemon.zuser="N"
#droppedpokemon.pokemon=form.cleaned_data['addedpokemonBBB']
#droppedpokemon.save()
