from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime, timedelta,timezone
import math
from django.db.models import Q
from django.contrib.auth.models import User

from leagues.models import *
from individualleague.models import *
from pokemonadmin.models import *
from pokemondatabase import *

from pokemondraftleague.celery import app

@shared_task(name = "award_check")
def award_check():
    admin=User.objects.get(username="Professor_Oak")
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
                messagebody=f'Congratulations! You have been awarded a trophy for winning a championship. Check it out at https://www.pokemondraftleague.online/users/{winner.coach.username}'
                awardcheck(winner.coach,awardtogive,awardtext,messagebody,admin)
                if winner.teammate != None:
                    messagebody=f'Congratulations! You have been awarded a trophy for winning a championship. Check it out at https://www.pokemondraftleague.online/users/{winner.teammate.username}'
                    awardcheck(winner.teammate,awardtogive,awardtext,messagebody,admin)
                awardtogive=award.objects.get(awardname="Runnerup")    
                messagebody=f'Congratulations! You have been awarded a trophy for coming in second place in a season. Check it out at https://www.pokemondraftleague.online/users/{runnerup.coach.username}'
                awardcheck(runnerup.coach,awardtogive,awardtext,messagebody,admin)
                if runnerup.teammate != None:
                    messagebody=f'Congratulations! You have been awarded a trophy for coming in second place in a season. Check it out at https://www.pokemondraftleague.online/users/{runnerup.teammate.username}'
                    awardcheck(runnerup.teammate,awardtogive,awardtext,messagebody,admin)
            except:
                print('Finals not played')
            #check third place
            try:
                awardtogive=award.objects.get(awardname="Thirdplace")
                thirdplacematch=schedule.objects.all().filter(season=s).exclude(winner__isnull=True).get(week="Playoffs Third Place Match")
                winner=thirdplacematch.winner
                messagebody=f'Congratulations! You have been awarded a trophy for coming in third place in a season. Check it out at https://www.pokemondraftleague.online/users/{winner.coach.username}'
                awardcheck(winner.coach,awardtogive,awardtext,messagebody,admin)
                if winner.teammate != None:
                    messagebody=f'Congratulations! You have been awarded a trophy for coming in third place in a season. Check it out at https://www.pokemondraftleague.online/users/{winner.teammate.username}'
                    awardcheck(winner.teammate,awardtogive,awardtext,messagebody,admin)
            except:
                print('Third place match not played')
            ##check playoffs
            awardtogive=award.objects.get(awardname="Playoffs")
            season_playoffmatches=schedule.objects.all().filter(season=s,week__contains="Playoffs").exclude(winner__isnull=True).distinct('winner')
            for m in season_playoffmatches:
                messagebody=f'Congratulations! You have been awarded a trophy for making playoffs in a season. Check it out at https://www.pokemondraftleague.online/users/{m.team1.coach.username}'
                awardcheck(m.team1.coach,awardtogive,awardtext,messagebody,admin)
                messagebody=f'Congratulations! You have been awarded a trophy for making playoffs in a season. Check it out at https://www.pokemondraftleague.online/users/{m.team2.coach.username}'
                awardcheck(m.team2.coach,awardtogive,awardtext,messagebody,admin)
                if m.team1.teammate != None: 
                    messagebody=f'Congratulations! You have been awarded a trophy for making playoffs in a season. Check it out at https://www.pokemondraftleague.online/users/{m.team1.teammate.username}'
                    awardcheck(m.team1.teammate,awardtogive,awardtext,messagebody,admin)
                if m.team2.teammate != None: 
                    messagebody=f'Congratulations! You have been awarded a trophy for making playoffs in a season. Check it out at https://www.pokemondraftleague.online/users/{m.team2.teammate.username}'
                    awardcheck(m.team2.teammate,awardtogive,awardtext,messagebody,admin)       
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
                messagebody=f'Congratulations! You have been awarded a trophy for winning a championship. Check it out at https://www.pokemondraftleague.online/users/{winner.coach1.username}'
                awardcheck(winner.coach1,awardtogive,awardtext,messagebody,admin)
                if winner.coach2 != None:
                    messagebody=f'Congratulations! You have been awarded a trophy for winning a championship. Check it out at https://www.pokemondraftleague.online/users/{winner.coach2.username}'
                    awardcheck(winner.coach2,awardtogive,awardtext,messagebody,admin)
                awardtogive=award.objects.get(awardname="Runnerup")    
                messagebody=f'Congratulations! You have been awarded a trophy for coming in second place in a season. Check it out at https://www.pokemondraftleague.online/users/{runnerup.coach1.username}'
                awardcheck(runnerup.coach1,awardtogive,awardtext,messagebody,admin)
                if runnerup.coach2 != None:
                    messagebody=f'Congratulations! You have been awarded a trophy for coming in second place in a season. Check it out at https://www.pokemondraftleague.online/users/{runnerup.coach2.username}'
                    awardcheck(runnerup.coach2,awardtogive,awardtext,messagebody,admin)
            except:
                print('Finals not played')
            #check third place
            try:
                awardtogive=award.objects.get(awardname="Thirdplace")
                thirdplacematch=historical_match.objects.all().filter(team1__seasonname=s.seasonname).exclude(winner__isnull=True).get(week="Playoffs Third Place Match")
                winner=thirdplacematch.winner
                messagebody=f'Congratulations! You have been awarded a trophy for coming in third place in a season. Check it out at https://www.pokemondraftleague.online/users/{winner.coach1.username}'
                awardcheck(winner.coach1,awardtogive,awardtext,messagebody,admin)
                if winner.coach2 != None:
                    messagebody=f'Congratulations! You have been awarded a trophy for coming in third place in a season. Check it out at https://www.pokemondraftleague.online/users/{winner.coach2.username}'
                    awardcheck(winner.coach2,awardtogive,awardtext,messagebody,admin)
            except:
                print('Third place match not played')
            ##check playoffs
            awardtogive=award.objects.get(awardname="Playoffs")
            season_playoffmatches=historical_match.objects.all().filter(team1__seasonname=s.seasonname,week__contains="Playoffs").exclude(winner__isnull=True).distinct('winner')
            awardtext=f'{item.name} {s.seasonname}'
            for m in season_playoffmatches:
                messagebody=f'Congratulations! You have been awarded a trophy for making playoffs in a season. Check it out at https://www.pokemondraftleague.online/users/{m.team1.coach1.username}'
                awardcheck(m.team1.coach1,awardtogive,awardtext,messagebody,admin)
                messagebody=f'Congratulations! You have been awarded a trophy for making playoffs in a season. Check it out at https://www.pokemondraftleague.online/users/{m.team2.coach1.username}'
                awardcheck(m.team2.coach1,awardtogive,awardtext,messagebody,admin)
                if m.team1.coach2 != None: 
                    messagebody=f'Congratulations! You have been awarded a trophy for making playoffs in a season. Check it out at https://www.pokemondraftleague.online/users/{m.team1.coach2.username}'
                    awardcheck(m.team1.coach2,awardtogive,awardtext,messagebody,admin)
                if m.team2.coach2 != None: 
                    messagebody=f'Congratulations! You have been awarded a trophy for making playoffs in a season. Check it out at https://www.pokemondraftleague.online/users/{m.team2.coach2.username}'
                    awardcheck(m.team2.coach2,awardtogive,awardtext,messagebody,admin)
        all_users=User.objects.all()
    
    #check season participation
    admin=User.objects.get(username="Professor_Oak")
    for u in all_users:
        active=coachdata.objects.all().filter(Q(coach=u)|Q(teammate=u)).exclude(league_name__name__contains="Test")
        past=historical_team.objects.all().filter(Q(coach1=u)|Q(coach2=u)).exclude(league__name__contains="Test")
        teams=league_team.objects.all().filter(alternate=u)
        seasoncount=active.count()+past.count()+teams.count()
        awardtext='Pokemon Draft League'
        if seasoncount>0:
            messagebody=f'Congratulations! You have been awarded a trophy for participating in at least one season. Check it out at https://www.pokemondraftleague.online/users/{u.username}'
            awardtogive=award.objects.get(awardname="1 Season Played")
            awardcheck(u,awardtogive,awardtext,messagebody,admin)
        if seasoncount>2:
            messagebody=f'Congratulations! You have been awarded a trophy for participating in at least three seasons. Check it out at https://www.pokemondraftleague.online/users/{u.username}'
            awardtogive=award.objects.get(awardname="3 Seasons Played")
            awardcheck(u,awardtogive,awardtext,messagebody,admin)
        if seasoncount>4:
            awardtogive=award.objects.get(awardname="5 Seasons Played")
            awardcheck(u,awardtogive,awardtext,messagebody,admin)
            messagebody=f'Congratulations! You have been awarded a trophy for participating in at least five seasons. Check it out at https://www.pokemondraftleague.online/users/{u.username}'
        if seasoncount>9:
            awardtogive=award.objects.get(awardname="10 Seasons Played")
            awardcheck(u,awardtogive,awardtext,messagebody,admin)
            messagebody=f'Congratulations! You have been awarded a trophy for participating in at least ten seasons. Check it out at https://www.pokemondraftleague.online/users/{u.username}'

def awardcheck(coach,awardtogive,awardtext,messagebody,admin):
    try:
        coachaward.objects.filter(coach=coach, award=awardtogive).get(text=awardtext)
    except:
        inbox.objects.create(sender=admin,recipient=coach,messagesubject='You have been awarded a trophy!', messagebody=messagebody)
        coachaward.objects.create(coach=coach,award=awardtogive,text=awardtext)
      