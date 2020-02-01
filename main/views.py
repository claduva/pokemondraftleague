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
import math

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
    roster.objects.all().update(kills=0,deaths=0,differential=0,gp=0,gw=0,support=0,damagedone=0,hphealed=0,luck=0,remaininghealth=0)
    historical_roster.objects.all().update(kills=0,deaths=0,differential=0,gp=0,gw=0,support=0,damagedone=0,hphealed=0,luck=0,remaininghealth=0)
    all_pokemon.objects.all().update(kills=0,deaths=0,differential=0,gp=0,gw=0,support=0,damagedone=0,hphealed=0,luck=0,remaininghealth=0)
    ##zero coachs
    coachdata.objects.all().update(wins=0,losses=0,differential=0,forfeit=0,support=0,damagedone=0,hphealed=0,luck=0,remaininghealth=0)
    historical_team.objects.all().update(wins=0,losses=0,differential=0,forfeit=0,support=0,damagedone=0,hphealed=0,luck=0,remaininghealth=0)
    return redirect('home')

@check_if_clad
def updatematches(request):
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

    return redirect('home')