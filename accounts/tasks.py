from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime, timedelta,timezone
import math
from django.db.models import Q

from leagues.models import *
from individualleague.models import *
from pokemonadmin.models import *
from pokemondatabase import *

from pokemondraftleague.celery import app

@shared_task(name = "award_check")
def award_check():
    
    
    ##check playoffs
    awardtogive=award.objects.get(awardname="Playoffs")
    all_leagues=league.objects.all()
    for item in all_leagues:       
        #current seasons
        currentseason=seasonsetting.objects.all().filter(league=item)
        for s in currentseason:
            season_playoffmatches=schedule.objects.all().filter(season=s,week__contains="Playoffs").exclude(winner__isnull=True).distinct('winner')
            awardtext=f'{item.name} {s.seasonname}'
            for m in season_playoffmatches:
                try:
                    coachaward.objects.filter(coach=m.team1.coach, award__awardname="Playoffs").get(text=awardtext)
                except:
                    print('nomatch')
                    coachaward.objects.create(coach=m.team1.coach,award=awardtogive,text=awardtext)
                try:
                    coachaward.objects.filter(coach=m.team2.coach, award__awardname="Playoffs").get(text=awardtext)
                except:
                    print('nomatch')
                    coachaward.objects.create(coach=m.team2.coach,award=awardtogive,text=awardtext)
                if m.team1.teammate != None: 
                    try:
                        coachaward.objects.filter(coach=m.team1.teammate, award__awardname="Playoffs").get(text=awardtext)
                    except:
                        print('nomatch')
                        coachaward.objects.create(coach=m.team1.teammate,award=awardtogive,text=awardtext)
                if m.team2.teammate != None: 
                    try:
                        coachaward.objects.filter(coach=m.team2.teammate, award__awardname="Playoffs").get(text=awardtext)
                    except:
                        print('nomatch')
                        coachaward.objects.create(coach=m.team2.teammate,award=awardtogive,text=awardtext)        
        #historical seasons
        historical_seasons=historical_team.objects.all().filter(league=item).distinct('seasonname')
        for s in historical_seasons:
            season_playoffmatches=historical_match.objects.all().filter(team1__seasonname=s.seasonname,week__contains="Playoffs").exclude(winner__isnull=True).distinct('winner')
            awardtext=f'{item.name} {s.seasonname}'
            for m in season_playoffmatches:
                try:
                    coachaward.objects.filter(coach=m.team1.coach1, award__awardname="Playoffs").get(text=awardtext)
                except:
                    print('nomatch')
                    coachaward.objects.create(coach=m.team1.coach1,award=awardtogive,text=awardtext)
                try:
                    coachaward.objects.filter(coach=m.team2.coach1, award__awardname="Playoffs").get(text=awardtext)
                except:
                    print('nomatch')
                    coachaward.objects.create(coach=m.team2.coach1,award=awardtogive,text=awardtext)
                if m.team1.coach2 != None: 
                    try:
                        coachaward.objects.filter(coach=m.team1.coach2, award__awardname="Playoffs").get(text=awardtext)
                    except:
                        print('nomatch')
                        coachaward.objects.create(coach=m.team1.coach2,award=awardtogive,text=awardtext)
                if m.team2.coach2 != None: 
                    try:
                        coachaward.objects.filter(coach=m.team2.coach2, award__awardname="Playoffs").get(text=awardtext)
                    except:
                        print('nomatch')
                        coachaward.objects.create(coach=m.team2.coach2,award=awardtogive,text=awardtext)

  
      