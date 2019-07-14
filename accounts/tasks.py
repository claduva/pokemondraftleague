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
    all_leagues=league.objects.all()
    for item in all_leagues:       
        #current seasons
        currentseason=seasonsetting.objects.all().filter(league=item)
        for s in currentseason:
            awardtext=f'{item.name} {s.seasonname}'
            #check finals 
            try:
                awardtogive=award.objects.get(awardname="Champion")
                finalsmatch=schedule.objects.all().filter(season=s).exclude(winner__isnull=True).get(week="Playoffs Finals")
                winner=finalsmatch.winner
                if winner==finalsmatch.team1: runnerup=finalsmatch.team2 
                else: runnerup=finalsmatch.team1
                awardcheck(winner.coach,awardtogive,awardtext)
                if winner.teammate != None:
                    awardcheck(winner.teammate,awardtogive,awardtext)
                awardtogive=award.objects.get(awardname="Runnerup")    
                awardcheck(runnerup.coach,awardtogive,awardtext)
                if runnerup.teammate != None:
                    awardcheck(runnerup.teammate,awardtogive,awardtext)
            except:
                print('Finals not played')
            #check third place
            try:
                awardtogive=award.objects.get(awardname="Thirdplace")
                thirdplacematch=schedule.objects.all().filter(season=s).exclude(winner__isnull=True).get(week="Playoffs Third Place Match")
                winner=thirdplacematch.winner
                awardcheck(winner.coach,awardtogive,awardtext)
                if winner.teammate != None:
                    awardcheck(winner.teammate,awardtogive,awardtext)
            except:
                print('Third place match not played')
            ##check playoffs
            awardtogive=award.objects.get(awardname="Playoffs")
            season_playoffmatches=schedule.objects.all().filter(season=s,week__contains="Playoffs").exclude(winner__isnull=True).distinct('winner')
            for m in season_playoffmatches:
                awardcheck(m.team1.coach,awardtogive,awardtext)
                awardcheck(m.team2.coach,awardtogive,awardtext)
                if m.team1.teammate != None: 
                    awardcheck(m.team1.teammate,awardtogive,awardtext)
                if m.team2.teammate != None: 
                    awardcheck(m.team2.teammate,awardtogive,awardtext)       
        #historical seasons
        historical_seasons=historical_team.objects.all().filter(league=item).distinct('seasonname')
        for s in historical_seasons:
            awardtext=f'{item.name} {s.seasonname}'
            #check finals 
            try:
                awardtogive=award.objects.get(awardname="Champion")
                finalsmatch=historical_match.objects.all().filter(team1__seasonname=s.seasonname).exclude(winner__isnull=True).get(week="Playoffs Finals")
                winner=finalsmatch.winner
                if winner==finalsmatch.team1: runnerup=finalsmatch.team2 
                else: runnerup=finalsmatch.team1
                awardcheck(winner.coach1,awardtogive,awardtext)
                if winner.coach2 != None:
                    awardcheck(winner.coach2,awardtogive,awardtext)
                awardtogive=award.objects.get(awardname="Runnerup")    
                awardcheck(runnerup.coach1,awardtogive,awardtext)
                if runnerup.coach2 != None:
                    awardcheck(runnerup.coach2,awardtogive,awardtext)
            except:
                print('Finals not played')
            #check third place
            try:
                awardtogive=award.objects.get(awardname="Thirdplace")
                thirdplacematch=historical_match.objects.all().filter(team1__seasonname=s.seasonname).exclude(winner__isnull=True).get(week="Playoffs Third Place Match")
                winner=thirdplacematch.winner
                awardcheck(winner.coach1,awardtogive,awardtext)
                if winner.coach2 != None:
                    awardcheck(winner.coach2,awardtogive,awardtext)
            except:
                print('Third place match not played')
            ##check playoffs
            awardtogive=award.objects.get(awardname="Playoffs")
            season_playoffmatches=historical_match.objects.all().filter(team1__seasonname=s.seasonname,week__contains="Playoffs").exclude(winner__isnull=True).distinct('winner')
            awardtext=f'{item.name} {s.seasonname}'
            for m in season_playoffmatches:
                awardcheck(m.team1.coach1,awardtogive,awardtext)
                awardcheck(m.team2.coach1,awardtogive,awardtext)
                if m.team1.coach2 != None: 
                    awardcheck(m.team1.coach2,awardtogive,awardtext)
                if m.team2.coach2 != None: 
                    awardcheck(m.team2.coach2,awardtogive,awardtext)

def awardcheck(coach,awardtogive,awardtext):
    try:
        coachaward.objects.filter(coach=coach, award=awardtogive).get(text=awardtext)
    except:
        coachaward.objects.create(coach=coach,award=awardtogive,text=awardtext) 
      