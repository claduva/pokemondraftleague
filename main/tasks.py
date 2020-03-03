from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime, timedelta,timezone
import math
from django.db.models import Q

from pokemondraftleague.celery import app
from leagues.models import seasonsetting
from individualleague.models import *
from pokemonadmin.models import *

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