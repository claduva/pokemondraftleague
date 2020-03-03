from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime, timedelta,timezone
import math
from django.db.models import Q

from pokemondraftleague.celery import app

from .models import free_agency, trading
from leagues.models import seasonsetting
from individualleague.models import *
from pokemonadmin.models import *

@shared_task(name = "print_msg_test")
def print_message_test():
  print("Celery is working!!")

@shared_task(name = "run_pickems")
def run_pickems():
  pass
  """
  leaderboard=pickem_leaderboard.objects.all()
  for item in leaderboard:
      item.submitted=0
      item.numbercorrect=0
      item.matchescompleted=0
      item.save()
      pickemlist=item.user.pickems.all()
      for p in pickemlist:
          item.submitted+=1
          if p.match.replay != "Link":
              item.matchescompleted+=1
              if p.pick==p.match.winner:
                  item.numbercorrect+=1
      item.save()
  """

@shared_task(name = "execute_fa_and_trades")
def execute_free_agency_and_trades():
  #free agencies
  unexecutedfa=free_agency.objects.all().filter(executed=False).order_by('id')
  #check if completed matches
  for item in unexecutedfa:
    request_league=seasonsetting.objects.get(subleague=item.season.subleague)
    requestedweek=item.weekeffective
    completedmatches=True
    if requestedweek >=2:
      for i in range(1,requestedweek):
        try:
          matchofinterest=schedule.objects.filter(season=item.season).filter(Q(team1=item.coach)|Q(team2=item.coach)).get(week=str(i))
          if matchofinterest.replay=="Link":
            completedmatches=False
        except:
          print('Match not found')
    if completedmatches:
      #execute free agencies
      montoupdate=item.droppedpokemon
      try:
        droppedpokemon=roster.objects.filter(season=item.season,team=item.coach).get(pokemon=item.droppedpokemon)
        item.executed=True
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
        montoupdate.support=droppedpokemon.support
        droppedpokemon.support=0
        montoupdate.hphealed=droppedpokemon.hphealed
        droppedpokemon.hphealed=0
        montoupdate.luck=droppedpokemon.luck
        droppedpokemon.luck=0
        montoupdate.damagedone=droppedpokemon.damagedone
        droppedpokemon.damagedone=0
        montoupdate.remaininghealth=droppedpokemon.remaininghealth
        droppedpokemon.remaininghealth=0
        droppedpokemon.zuser="N"     
        droppedpokemon.pokemon=item.addedpokemon
      except:
        try:
          droppedpokemon=roster.objects.filter(season=item.season,team=item.coach).get(pokemon=item.addedpokemon)
          item.executed=True
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
          montoupdate.support=droppedpokemon.support
          droppedpokemon.support=0
          montoupdate.hphealed=droppedpokemon.hphealed
          droppedpokemon.hphealed=0
          montoupdate.luck=droppedpokemon.luck
          droppedpokemon.luck=0
          montoupdate.damagedone=droppedpokemon.damagedone
          droppedpokemon.damagedone=0
          montoupdate.remaininghealth=droppedpokemon.remaininghealth
          droppedpokemon.remaininghealth=0
          droppedpokemon.zuser="N"  
        except:
          pass
      item.save()
      droppedpokemon.save() 
      montoupdate.save()
  #trades
  unexecutedtrades=trading.objects.all().filter(executed=False).order_by('id')
  print(unexecutedtrades)
  #check if completed matches
  for item in unexecutedtrades:
    request_league=seasonsetting.objects.get(subleague=item.season.subleague)
    requestedweek=item.weekeffective
    completedmatches=True
    if requestedweek >= 2:
      for i in range(1,requestedweek):
        try:
          matchofinterest=schedule.objects.filter(season=item.season).filter(Q(team1=item.coach)|Q(team2=item.coach)).get(week=str(i))
          if matchofinterest.replay=="Link":
            completedmatches=False
        except:
          print('Match not found')
    if completedmatches:
      #execute trades
      montoupdate=item.droppedpokemon
      try:
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
        montoupdate.support=droppedpokemon.support
        droppedpokemon.support=0
        montoupdate.hphealed=droppedpokemon.hphealed
        droppedpokemon.hphealed=0
        montoupdate.luck=droppedpokemon.luck
        droppedpokemon.luck=0
        montoupdate.damagedone=droppedpokemon.damagedone
        droppedpokemon.damagedone=0
        montoupdate.remaininghealth=droppedpokemon.remaininghealth
        droppedpokemon.remaininghealth=0
        droppedpokemon.zuser="N"
        droppedpokemon.pokemon=item.addedpokemon
        item.executed=True
      except:
        try:
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
          montoupdate.support=droppedpokemon.support
          droppedpokemon.support=0
          montoupdate.hphealed=droppedpokemon.hphealed
          droppedpokemon.hphealed=0
          montoupdate.luck=droppedpokemon.luck
          droppedpokemon.luck=0
          montoupdate.damagedone=droppedpokemon.damagedone
          droppedpokemon.damagedone=0
          montoupdate.remaininghealth=droppedpokemon.remaininghealth
          droppedpokemon.remaininghealth=0
          droppedpokemon.zuser="N"
          item.executed=True
        except:
          pass
      item.save()
      droppedpokemon.save() 
      montoupdate.save()

@shared_task(name = "run_replay_database")
def run_replay_database():
  current=schedule.objects.all().exclude(replay="Link")
  prior=historical_match.objects.all()
  total=current.count()+prior.count()
  counter=1
  for match in current:
    if match.team1alternateattribution:
      a=match.team1alternateattribution
      b=None
    else:
      a=match.team1.coach
      b=match.team1.teammate
    if match.team2alternateattribution:
      c=match.team2alternateattribution
      d=None
    else:
      c=match.team2.coach
      d=match.team2.teammate
    if match.winneralternateattribution:
      e=match.winneralternateattribution
      f=None
    else:
      try:
        e=match.winner.coach
        f=match.winner.teammate
      except:
        e=None
        f=None
    try:
      g=match.match_replay.data['team1']['coach']
      h=match.match_replay.data['team2']['coach']
    except:
      g="N/A"
      h="N/A"
    i=match.replay
    #
    try:
      databaseitem=match.replaydatabase
      databaseitem.team1coach1=a
      databaseitem.team1coach2=b
      databaseitem.team2coach1=c
      databaseitem.team2coach2=d
      databaseitem.winnercoach1=e
      databaseitem.winnercoach2=f
      databaseitem.replayuser1=g
      databaseitem.replayuser2=h
      databaseitem.replay=i
      databaseitem.save()
    except:
      replaydatabase.objects.create(
        associatedmatch=match,
        team1coach1=a,
        team1coach2=b,
        team2coach1=c,
        team2coach2=d,
        winnercoach1=e,
        winnercoach2=f,
        replayuser1=g,
        replayuser2=h,
        replay=i,
      )
    print(f'{counter}/{total}')
    counter+=1
  for match in prior:
    if match.team1alternateattribution:
      a=match.team1alternateattribution
      b=None
    else:
      a=match.team1.coach1
      b=match.team1.coach2
    if match.team2alternateattribution:
      c=match.team2alternateattribution
      d=None
    else:
      c=match.team2.coach1
      d=match.team2.coach2
    if match.winneralternateattribution:
      e=match.winneralternateattribution
      f=None
    else:
      try:
        e=match.winner.coach1
        f=match.winner.coach2
      except:
        e=None
        f=None
    try:
      g=match.historical_match_replay.data['team1']['coach']
      h=match.historical_match_replay.data['team2']['coach']
    except:
      g="N/A"
      h="N/A"
    i=match.replay
    #
    try:
      databaseitem=replaydatabase.objects.get(associatedhistoricmatch=match)
      databaseitem.team1coach1=a
      databaseitem.team1coach2=b
      databaseitem.team2coach1=c
      databaseitem.team2coach2=d
      databaseitem.winnercoach1=e
      databaseitem.winnercoach2=f
      databaseitem.replayuser1=g
      databaseitem.replayuser2=h
      databaseitem.replay=i
      databaseitem.save()
    except:
      replaydatabase.objects.create(
        associatedhistoricmatch=match,
        team1coach1=a,
        team1coach2=b,
        team2coach1=c,
        team2coach2=d,
        winnercoach1=e,
        winnercoach2=f,
        replayuser1=g,
        replayuser2=h,
        replay=i,
      )
    print(f'{counter}/{total}')
    counter+=1