from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
from django.db.models import Q
from django.core.files.base import ContentFile

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

def replay_database(request):
    database=replaydatabase.objects.all()
    context = {
        'database':database,
    }
    return render(request,"replay_database.html",context)

def runscript(request): 
    current=schedule.objects.all().exclude(replay="Link")
    prior=historical_match.objects.all()
    total=current.count()+prior.count()
    counter=1
    """
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
    """
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
    return redirect('home')