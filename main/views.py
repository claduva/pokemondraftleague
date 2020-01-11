from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
from django.db.models import Q

import json
from datetime import datetime
import time
import csv
import os
import requests

from accounts.forms import UserRegisterForm
from .models import *
from accounts.models import *
from leagues.models import *
from individualleague.models import *
from pokemonadmin.models import *
from pokemondatabase.models import *

from replayanalysis.NewParser.parser import *
from replayanalysis.models import *
from replayanalysis.ShowdownReplayParser.replayparser import *
from replayanalysis.helperfunctions import *
from pokemondraftleague.customdecorators import check_if_clad

def home(request):
    try:
        yourleagues=coachdata.objects.all().filter(Q(coach=request.user)|Q(teammate=request.user))
        if yourleagues.count()>0:
            upcomingmatches=schedule.objects.all().filter(Q(team1__coach=request.user)|Q(team2__coach=request.user)|Q(team1__teammate=request.user)|Q(team2__teammate=request.user)).filter(replay="Link").order_by('duedate','id')[0:4]
            recentresults=schedule.objects.all().filter(Q(team1__coach=request.user)|Q(team2__coach=request.user)|Q(team1__teammate=request.user)|Q(team2__teammate=request.user)).exclude(replay="Link").exclude(Q(team1__coach=request.user)|Q(team1__teammate=request.user),team1alternateattribution__isnull=False).exclude(Q(team2__coach=request.user)|Q(team2__teammate=request.user),team2alternateattribution__isnull=False).order_by('-timestamp','-id')[0:4]
            context = {
                "title": "Pokemon Draft League",
                "yourleagues": yourleagues,
                "upcomingmatches":upcomingmatches,
                "recentresults": recentresults,
            }
            return  render(request,"coachlandingpage.html", context)
    except Exception as e:
        print(e)
    form=UserRegisterForm()
    context = {
        "title": "Pokemon Draft League",
        "form": form,
    }
    return  render(request,"index.html", context)

def about(request):
    coachs=[]
    coachlist=coachdata.objects.all().exclude(league_name__name__contains="Test")
    for c in coachlist:
        if c.coach.username not in coachs:
            coachs.append(c.coach.username)
        if c.teammate and c.teammate.username not in coachs:
            coachs.append(c.teammate.username) 
    coachlist=historical_team.objects.all().exclude(coach1__username="UnclaimedCoach")
    for c in coachlist:
        if c.coach1.username not in coachs:
            coachs.append(c.coach1.username)
        if c.coach2 and c.coach2.username not in coachs:
            coachs.append(c.coach2.username) 
    leagues=league.objects.all().exclude(name__contains="Test")
    historicalmatches=historical_match.objects.all().exclude(replay="").exclude(replay__contains="FF")
    currentmatches=schedule.objects.all().exclude(replay="Link").exclude(replay__contains="FF")
    seasonscompleted=0
    for l in leagues:
        seasonscompleted+=historical_team.objects.all().filter(league=l).distinct('seasonname').count()
    context = {
        "numberofleagues":leagues.count(),
        "uniquecoaches": len(coachs),
        "seasonscompleted":seasonscompleted,
        "matchesplayed": currentmatches.count()+historicalmatches.count(),
    }
    return  render(request,"about.html", context)

def custom404(request,exception):
    return  render(request,"404.html")

def custom500(request,exception):
    return  render(request,"500.html")

def discordbotpage(request):
    return  render(request,"discordbot.html")

def pokemonleaderboard(request):
    leaderboard=pokemon_leaderboard.objects.all().filter(gp__gt=0).order_by('-kills','-differential')
    context = {
        "title": "Pokemon Leaderboard",
        "leaderboard": leaderboard
    }
    return  render(request,"pokemonleaderboard.html",context)

def userleaderboard(request):
    leaderboard=profile.objects.all().filter(Q(wins__gt=0)|Q(losses__gt=0)).order_by('-wins','-differential').exclude(user__username="UnclaimedCoach")
    context = {
        "title": "User Leaderboard",
        "leaderboard": leaderboard
    }
    return  render(request,"userleaderboard.html",context)

def pickemleaderboard(request):
    leaderboard=pickem_leaderboard.objects.all().order_by('-numbercorrect').exclude(matchescompleted__lt=1)
    context = {
        "title": "Pickem Leaderboard",
        "leaderboard": leaderboard
    }
    return  render(request,"pickemleaderboard.html",context)

@check_if_clad
def zerorosters(request):
##zero rosters
    items=roster.objects.all()
    for item in items:
        item.kills=0; item.deaths=0; item.differential=0; item.gp=0; item.gw=0; item.support=0; item.damagedone=0; item.hphealed=0; item.luck=0; item.remaininghealth=0
        item.save()
    items=historical_roster.objects.all()
    for item in items:
        item.kills=0; item.deaths=0; item.differential=0; item.gp=0; item.gw=0; item.support=0; item.damagedone=0; item.hphealed=0; item.luck=0; item.remaininghealth=0
        item.save()
    items=all_pokemon.objects.all()
    for item in items:
        item.kills=0; item.deaths=0; item.differential=0; item.gp=0; item.gw=0; item.support=0; item.damagedone=0; item.hphealed=0; item.luck=0; item.remaininghealth=0
        item.save()
    ##zero coachs
    items=coachdata.objects.all()
    for item in items:
        item.wins=0; item.losses=0; item.differential=0; item.forfeit=0; item.support=0; item.damagedone=0; item.hphealed=0; item.luck=0; item.remaininghealth=0
        item.save()
    items=historical_team.objects.all()
    for item in items:
        item.wins=0; item.losses=0; item.differential=0; item.forfeit=0; item.support=0; item.damagedone=0; item.hphealed=0; item.luck=0; item.remaininghealth=0
        item.save()
    return redirect('home')

@check_if_clad
def updatematches(request):
    """
    i=0
    ##iterate through existing matches
    replays=match_replay.objects.all()
    for m in replays:
        i+=1
        print(i)
        match=m.match
        data=m.data
        #align coachs
        winner=match.winner
        team1=match.team1
        team2=match.team2
        if (team1==winner and data['team2']['wins']>0) or (team2==winner and data['team1']['wins']>0):
            team1=match.team2
            team2=match.team1
        #update teams
        team1.wins+=data['team1']['wins']; team1.losses+=abs(data['team1']['wins']-1); team1.differential+=data['team1']['kills']-data['team1']['deaths']; team1.forfeit=data['team1']['forfeit']
        team2.wins+=data['team2']['wins']; team2.losses+=abs(data['team2']['wins']-1); team2.differential+=data['team2']['kills']-data['team2']['deaths']; team2.forfeit=data['team2']['forfeit']
        ##
        for mon in data['team1']['roster']:
            searchmon=mon['pokemon']
            #search for mon
            try:
                foundmon=roster.objects.all().filter(season__subleague=team1.subleague,team=team1).get(pokemon__pokemon=searchmon)
            except:
                try:
                    foundmon=roster.objects.all().filter(season__subleague=team1.subleague,team=team1).get(pokemon__pokemon__contains=searchmon)
                except:
                    try:
                        foundmon=roster.objects.all().filter(season__subleague=team1.subleague).get(pokemon__pokemon=searchmon)
                    except:
                        try:
                            foundmon=roster.objects.all().filter(season__subleague=team1.subleague).get(pokemon__pokemon__contains=searchmon)
                        except:
                            foundmon=all_pokemon.objects.all().get(pokemon=searchmon)
            #update foundmon
            foundmon.kills+=mon['kills']; foundmon.deaths+=mon['deaths']; foundmon.differential+=mon['kills']-mon['deaths']; foundmon.gp+=1; foundmon.gw+=data['team1']['wins']; foundmon.support+=mon['support']; foundmon.damagedone+=mon['damagedone']; foundmon.hphealed+=mon['hphealed']; foundmon.luck+=mon['luck']; foundmon.remaininghealth+=mon['remaininghealth']
            #update team
            team1.support+=mon['support']; team1.damagedone+=mon['damagedone']; team1.hphealed+=mon['hphealed']; team1.luck+=mon['luck']; team1.remaininghealth+=mon['remaininghealth']
            foundmon.save()
        for mon in data['team2']['roster']:
            searchmon=mon['pokemon']
            #search for mon
            try:
                foundmon=roster.objects.all().filter(season__subleague=team2.subleague,team=team2).get(pokemon__pokemon=searchmon)
            except:
                try:
                    foundmon=roster.objects.all().filter(season__subleague=team2.subleague,team=team2).get(pokemon__pokemon__contains=searchmon)
                except:
                    try:
                        foundmon=roster.objects.all().filter(season__subleague=team2.subleague).get(pokemon__pokemon=searchmon)
                    except:
                        try:
                            foundmon=roster.objects.all().filter(season__subleague=team2.subleague).get(pokemon__pokemon__contains=searchmon)
                        except:
                            foundmon=all_pokemon.objects.all().get(pokemon=searchmon)
            #update foundmon
            foundmon.kills+=mon['kills']; foundmon.deaths+=mon['deaths']; foundmon.differential+=mon['kills']-mon['deaths']; foundmon.gp+=1; foundmon.gw+=data['team2']['wins']; foundmon.support+=mon['support']; foundmon.damagedone+=mon['damagedone']; foundmon.hphealed+=mon['hphealed']; foundmon.luck+=mon['luck']; foundmon.remaininghealth+=mon['remaininghealth']
            #update team
            team2.support+=mon['support']; team2.damagedone+=mon['damagedone']; team2.hphealed+=mon['hphealed']; team2.luck+=mon['luck']; team2.remaininghealth+=mon['remaininghealth']
            foundmon.save()
        team1.save()
        team2.save()
    ##iterate through historic matches
    replays=historical_match_replay.objects.all()
    for m in replays: 
        i+=1
        print(i)
        match=m.match
        data=m.data
        #align coachs
        winner=match.winner
        team1=match.team1
        team2=match.team2
        if (team1==winner and data['team2']['wins']>0) or (team2==winner and data['team1']['wins']>0):
            team1=match.team2
            team2=match.team1
        #update teams
        team1.wins+=data['team1']['wins']; team1.losses+=abs(data['team1']['wins']-1); team1.differential+=data['team1']['kills']-data['team1']['deaths']; team1.forfeit=data['team1']['forfeit']
        team2.wins+=data['team2']['wins']; team2.losses+=abs(data['team2']['wins']-1); team2.differential+=data['team2']['kills']-data['team2']['deaths']; team2.forfeit=data['team2']['forfeit']
        ##
        for mon in data['team1']['roster']:
            searchmon=mon['pokemon']
            #search for mon
            try: 
                foundmon=historical_roster.objects.all().filter(team=team1).get(pokemon__pokemon=searchmon)
            except:
                try:
                    foundmon=historical_roster.objects.all().filter(team=team1).get(pokemon__pokemon__contains=searchmon)
                except:
                    try:
                        foundmon=historical_roster.objects.all().filter(team__seasonname=team1.seasonname,team__subseason=team1.subseason).get(pokemon__pokemon=searchmon)
                    except:
                        try:
                            foundmon=historical_roster.objects.all().filter(team__seasonname=team1.seasonname,team__subseason=team1.subseason).get(pokemon__pokemon__contains=searchmon)
                        except:
                            foundmon=all_pokemon.objects.all().get(pokemon=searchmon)
            #update foundmon
            foundmon.kills+=mon['kills']; foundmon.deaths+= mon['deaths']; foundmon.differential+=mon['kills']-mon['deaths']; foundmon.gp+=1; foundmon.gw+=data['team1']['wins']; foundmon.support+=mon['support']; foundmon.damagedone+=mon['damagedone']; foundmon.hphealed+=mon['hphealed']; foundmon.luck+=mon['luck']; foundmon.remaininghealth+=mon['remaininghealth']
            #update team
            team1.support+=mon['support']; team1.damagedone+=mon['damagedone']; team1.hphealed+=mon['hphealed']; team1.luck+=mon['luck']; team1.remaininghealth+=mon['remaininghealth']
            foundmon.save()
        for mon in data['team2']['roster']:
            searchmon=mon['pokemon']
            #search for mon
            try:
                foundmon=historical_roster.objects.all().filter(team=team2).get(pokemon__pokemon=searchmon)
            except:
                try:
                    foundmon=historical_roster.objects.all().filter(team=team2).get(pokemon__pokemon__contains=searchmon)
                except:
                    try:
                        foundmon=historical_roster.objects.all().filter(team__seasonname=team2.seasonname,team__subseason=team2.subseason).get(pokemon__pokemon=searchmon)
                    except:
                        try:
                            foundmon=historical_roster.objects.all().filter(team__seasonname=team2.seasonname,team__subseason=team2.subseason).get(pokemon__pokemon__contains=searchmon)
                        except:
                            foundmon=all_pokemon.objects.all().get(pokemon=searchmon)
            #update foundmon
            foundmon.kills+=mon['kills']; foundmon.deaths+= mon['deaths']; foundmon.differential+=mon['kills']-mon['deaths']; foundmon.gp+=1; foundmon.gw+=data['team2']['wins']; foundmon.support+=mon['support']; foundmon.damagedone+=mon['damagedone']; foundmon.hphealed+=mon['hphealed']; foundmon.luck+=mon['luck']; foundmon.remaininghealth+=mon['remaininghealth']
            #update team
            team2.support+=mon['support']; team2.damagedone+=mon['damagedone']; team2.hphealed+=mon['hphealed']; team2.luck+=mon['luck']; team2.remaininghealth+=mon['remaininghealth']
            foundmon.save()
        team1.save()
        team2.save()
    """
    """
    ffmatches=schedule.objects.all().exclude(replay="Link").exclude(replay__contains="replay.pokemonshowdown.com").exclude(replay__contains="cdn.discordapp.com")
    for item in ffmatches:
        team1=item.team1
        team2=item.team2
        if item.replay=="Both Teams Forfeit":
            team1.differential+=-6
            team2.differential+=-6
            team1.losses+=1
            team2.losses+=1
        elif item.replay=="Team 1 Forfeits":
            team1.differential+=-6
            team2.differential+=3
            team1.losses+=1
            team2.wins+=1
        elif item.replay=="Team 2 Forfeits":
            team2.differential+=-6
            team1.differential+=3
            team2.losses+=1
            team1.wins+=1
        team1.save()
        team2.save()
    ffmatches=historical_match.objects.all().exclude(replay="Link").exclude(replay__contains="replay.pokemonshowdown.com").exclude(replay__contains="cdn.discordapp.com").exclude(replay="N/A")
    for item in ffmatches:
        team1=item.team1
        team2=item.team2
        if item.replay=="Both Teams Forfeit":
            team1.differential+=-6
            team2.differential+=-6
            team1.losses+=1
            team2.losses+=1
        elif item.replay=="Team 1 Forfeits":
            team1.differential+=-6
            team2.differential+=3
            team1.losses+=1
            team2.wins+=1
        elif item.replay=="Team 2 Forfeits":
            team2.differential+=-6
            team1.differential+=3
            team2.losses+=1
            team1.wins+=1
        team1.save()
        team2.save()
        """
    return redirect('home')

def runscript(request): 
    #hr=historical_match.objects.all().exclude(replay__contains="pokemonshowdown").exclude(replay__contains="Forfeit")
    #for item in hr:
    #    print(item.replay)
    moi=schedule.objects.get(id=575)
    print(moi.replay)
    #moi.replay="https://pokemondraftleague.online/static/logfiles/Season_2_ASPL_collin_vs_young.txt"
    #moi.save()
    return redirect('home')