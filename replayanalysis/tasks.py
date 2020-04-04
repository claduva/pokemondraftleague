from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime, timedelta,timezone
import math
from django.db.models import Q

from pokemondraftleague.celery import app
from leagues.models import *
from individualleague.models import *
from pokemonadmin.models import *

@shared_task(name = "run_analyzer")
def run_analyzer():
    ##zero rosters  
    roster.objects.all().update(kills=0,deaths=0,differential=0,gp=0,gw=0,support=0,damagedone=0,hphealed=0,luck=0,remaininghealth=0)
    historical_roster.objects.all().update(kills=0,deaths=0,differential=0,gp=0,gw=0,support=0,damagedone=0,hphealed=0,luck=0,remaininghealth=0)
    all_pokemon.objects.all().update(kills=0,deaths=0,differential=0,gp=0,gw=0,support=0,damagedone=0,hphealed=0,luck=0,remaininghealth=0)
    ##zero coachs
    coachdata.objects.all().update(wins=0,losses=0,differential=0,forfeit=0,support=0,damagedone=0,hphealed=0,luck=0,remaininghealth=0)
    historical_team.objects.all().update(wins=0,losses=0,differential=0,forfeit=0,support=0,damagedone=0,hphealed=0,luck=0,remaininghealth=0)
    currentmatches=schedule.objects.all().filter(Q(replay__contains="replay.pokemonshowdown.com")|Q(replay__contains="/static/logfiles/"))
    histmatches=historical_match.objects.all().filter(Q(replay__contains="replay.pokemonshowdown.com")|Q(replay__contains="/static/logfiles/"))
    histffmatches=historical_match.objects.all().filter(replay__contains="Forfeit").order_by('id')
    ffmatches=schedule.objects.all().filter(replay__contains="Forfeit").order_by('id')
    unavailable=historical_match.objects.all().filter(replay="Unavailable")
    total=currentmatches.count()+histmatches.count()+histffmatches.count()+ffmatches.count()+unavailable.count()
    i=1
    #forfeits
    print('Forfeit')
    for item in ffmatches:
        team1=item.team1
        team2=item.team2
        if item.replay=="Both Teams Forfeit":
            team1.differential+=-3
            team2.differential+=-3
            team1.losses+=1
            team2.losses+=1
            team1.forfeit+=1
            team2.forfeit+=1
        elif item.replay=="Team 1 Forfeits":
            team1.differential+=-3
            team2.differential+=3
            team1.losses+=1
            team2.wins+=1
            team1.forfeit+=1
        elif item.replay=="Team 2 Forfeits":
            team2.differential+=-3
            team1.differential+=3
            team2.losses+=1
            team1.wins+=1
            team2.forfeit+=1
        team1.save()
        team2.save()
        print(f'{i}/{total}')
        i+=1
    for item in histffmatches:
        team1=item.team1
        team2=item.team2
        if item.replay=="Both Teams Forfeit":
            team1.differential+=-3
            team2.differential+=-3
            team1.losses+=1
            team2.losses+=1
            team1.forfeit+=1
            team2.forfeit+=1
        elif item.replay=="Team 1 Forfeits":
            team1.differential+=-3
            team2.differential+=3
            team1.losses+=1
            team2.wins+=1
            team1.forfeit+=1
        elif item.replay=="Team 2 Forfeits":
            team2.differential+=-3
            team1.differential+=3
            team2.losses+=1
            team1.wins+=1
            team2.forfeit+=1
        team1.save()
        team2.save()
        print(f'{i}/{total}')
        i+=1
    #unavailable
    print('Unavailable')
    for item in unavailable:
        team1=item.team1
        team2=item.team2
        team1.differential+=item.team1score-item.team2score
        team2.differential+=item.team2score-item.team1score
        if item.winner==item.team1:
            team1.wins+=1
            team2.losses+=1
        elif item.winner==item.team2:
            team2.wins+=1
            team1.losses+=1
        print(f'{i}/{total}')
        i+=1
    failed=[]
    print('Current')
    for item in currentmatches:
        try:
            check_current_match(item)
        except:
            failed.append(item)
        print(f'{i}/{total}')
        i+=1
    print('Historic')
    for item in histmatches:
        try:
            check_hist_match(item)
        except:
            failed.append(item)
        print(f'{i}/{total}')
        i+=1
    print('Failed')
    for item in failed:
        print(f'{item.id}: {item.replay}')

def update_current_match(mr):
    match=mr.match
    data=mr.data
    #align coachs
    winner=match.winner
    team1=match.team1
    team2=match.team2
    if (team1==winner and data['team2']['wins']>0) or (team2==winner and data['team1']['wins']>0):
        team1=match.team2
        team2=match.team1
    #update teams
    team1.wins+=data['team1']['wins']; team1.losses+=abs(data['team1']['wins']-1); team1.differential+=data['team1']['score']-data['team2']['score']; team1.forfeit=data['team1']['forfeit']
    team2.wins+=data['team2']['wins']; team2.losses+=abs(data['team2']['wins']-1); team2.differential+=data['team2']['score']-data['team1']['score']; team2.forfeit=data['team2']['forfeit']
    ##
    for mon in data['team1']['roster']:
        searchmon=mon['pokemon']
        #search for mon
        foundmon=current_searchmon(team1,searchmon)
        #update foundmon
        foundmon.kills+=mon['kills']; foundmon.deaths+=mon['deaths']; foundmon.differential+=mon['kills']-mon['deaths']; foundmon.gp+=1; foundmon.gw+=data['team1']['wins']; foundmon.support+=mon['support']; foundmon.damagedone+=mon['damagedone']; foundmon.hphealed+=mon['hphealed']; foundmon.luck+=mon['luck']; foundmon.remaininghealth+=mon['remaininghealth']
        #update team
        team1.support+=mon['support']; team1.damagedone+=mon['damagedone']; team1.hphealed+=mon['hphealed']; team1.luck+=mon['luck']; team1.remaininghealth+=mon['remaininghealth']
        foundmon.save()
    for mon in data['team2']['roster']:
        searchmon=mon['pokemon']
        #search for mon
        foundmon=current_searchmon(team2,searchmon)
        #update foundmon
        foundmon.kills+=mon['kills']; foundmon.deaths+=mon['deaths']; foundmon.differential+=mon['kills']-mon['deaths']; foundmon.gp+=1; foundmon.gw+=data['team2']['wins']; foundmon.support+=mon['support']; foundmon.damagedone+=mon['damagedone']; foundmon.hphealed+=mon['hphealed']; foundmon.luck+=mon['luck']; foundmon.remaininghealth+=mon['remaininghealth']
        #update team
        team2.support+=mon['support']; team2.damagedone+=mon['damagedone']; team2.hphealed+=mon['hphealed']; team2.luck+=mon['luck']; team2.remaininghealth+=mon['remaininghealth']
        foundmon.save()
    team1.save()
    team2.save()
    return 

def current_searchmon(toi,searchmon):
    try:
        foundmon=roster.objects.all().filter(season__subleague=toi.subleague,team=toi).get(pokemon__pokemon=searchmon)
    except:
        try:
            foundmon=roster.objects.all().filter(season__subleague=toi.subleague,team=toi).get(pokemon__pokemon__contains=searchmon)
        except:
            try:
                foundmon=roster.objects.all().filter(season__subleague=toi.subleague).get(pokemon__pokemon=searchmon)
            except:
                try:
                    foundmon=roster.objects.all().filter(season__subleague=toi.subleague).get(pokemon__pokemon__contains=searchmon)
                except:
                    foundmon=all_pokemon.objects.all().get(pokemon=searchmon)
    return foundmon

def historic_searchmon(toi,searchmon):
    try:
        foundmon=historical_roster.objects.all().filter(team=toi).get(pokemon__pokemon=searchmon)
    except:
        try:
            foundmon=historical_roster.objects.all().filter(team=toi).get(pokemon__pokemon__contains=searchmon)
        except:
            try:
                foundmon=historical_roster.objects.all().filter(team__seasonname=toi.seasonname,team__subseason=toi.subseason).get(pokemon__pokemon=searchmon)
            except:
                try:
                    foundmon=historical_roster.objects.all().filter(team__seasonname=toi.seasonname,team__subseason=toi.subseason).get(pokemon__pokemon__contains=searchmon)
                except:
                    foundmon=all_pokemon.objects.all().get(pokemon=searchmon)
    return foundmon