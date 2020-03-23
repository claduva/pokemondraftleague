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
from .forms import HelpForm

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
    database=replaydatabase.objects.all().order_by('team1coach1__username').values('team1coach1__username','team1coach2__username','team2coach1__username','team2coach2__username','winnercoach1__username','winnercoach2__username','replayuser1','replayuser2','winneruser','replay','associatedmatch','associatedhistoricmatch')
    print(database.count())
    database=list(database)
    r=json.dumps(database).replace('null', '""')
    database=json.loads(r)
    context = {
        'database':database,
        'user': request.user.username=="claduva"
    }
    return render(request,"replay_database.html",context)

@login_required
def help(request):
    form=HelpForm(initial={'sender':request.user,'recipient':User.objects.get(username='claduva')})
    if request.method == 'POST':
        form = HelpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your message has been sent! We will get back to you as soon as possible.')
            return redirect('help')
    context = {
        'form': form,
    }
    return render(request,"help.html",context)

def runscript(request): 
    ap=pokemon_effectiveness.objects.all()
    ap.update(bug=0,dark=0,dragon=0,electric=0,fairy=0,fighting=0,fire=0,flying=0,ghost=0,grass=0,ground=0,ice=0,normal=0,poison=0,psychic=0,rock=0,steel=0,water=0,)
    ap_=all_pokemon.objects.all()
    for item in ap_:
        try:
            item.effectiveness
        except:
            pokemon_effectiveness.objects.create(pokemon=item)
    j=1
    for i in ap:
        print(j)
        typing=i.pokemon.types.all()
        for t in typing:
            if t.typing=="Bug":
                i.fighting+=1
                i.flying+=-1
                i.ground+=1
                i.rock+=-1
                i.fire+=-1
                i.grass+=1
            elif t.typing=="Dark":
                i.fighting+=-1
                i.bug+=-1
                i.ghost+=1
                i.dark+=1
                i.fairy+=-1
            elif t.typing=="Dragon":
                i.fire+=1
                i.water+=1
                i.grass+=1
                i.electric+=1
                i.ice+=-1
                i.dragon+=-1
                i.fairy+=-1
            elif t.typing=="Electric":
                i.flying+=1
                i.ground+=-1
                i.steel+=1
                i.electric+=1
            elif t.typing=="Fairy":
                i.fighting+=1
                i.poison+=-1
                i.bug+=1
                i.steel+=-1
                i.dark+=1
            elif t.typing=="Fighting":
                i.flying+=-1
                i.rock+=1
                i.bug+=1
                i.psychic+=-1
                i.dark+=1
                i.fairy+=-1
            elif t.typing=="Fire":
                i.ground+=-1
                i.rock+=-1
                i.bug+=1
                i.steel+=1
                i.fire+=1
                i.water+=-1
                i.grass+=1
                i.ice+=1
                i.fairy+=1
            elif t.typing=="Flying":
                i.fighting+=1
                i.rock+=-1
                i.bug+=1
                i.grass+=1
                i.electric+=-1
                i.ice+=-1
            elif t.typing=="Ghost":
                i.poison+=1
                i.bug+=1
                i.dark+=-1
                i.ghost+=-1
            elif t.typing=="Grass":
                i.flying+=-1
                i.poison+=-1
                i.grass+=1
                i.ground+=1
                i.bug+=-1
                i.fire+=-1
                i.water+=1
                i.electric+=1
                i.ice+=-1
            elif t.typing=="Ground":
                i.poison+=1
                i.rock+=1
                i.water+=-1
                i.grass+=-1
                i.ice+=-1
            elif t.typing=="Ice":
                i.fighting+=-1
                i.steel+=-1
                i.fire+=-1
                i.rock+=-1
                i.ice+=1
            elif t.typing=="Normal":
                i.fighting+=-1
            elif t.typing=="Poison":
                i.fighting+=1
                i.poison+=1
                i.ground+=-1
                i.bug+=1
                i.grass+=1
                i.psychic+=-1
                i.fairy+=1
            elif t.typing=="Psychic":
                i.fighting+=1
                i.bug+=-1
                i.ghost+=-1
                i.dark+=-1
                i.psychic+=1
            elif t.typing=="Rock":
                i.normal+=1
                i.fighting+=-1
                i.flying+=1
                i.poison+=1
                i.ground+=-1
                i.steel+=-1
                i.fire+=1
                i.water+=-1
                i.grass+=-1
            elif t.typing=="Steel":
                i.normal+=1
                i.fighting+=-1
                i.flying+=1
                i.ground+=-1
                i.rock+=1
                i.bug+=1
                i.steel+=1
                i.fire+=-1
                i.grass+=1
                i.psychic+=1
                i.ice+=1
                i.dragon+=1
                i.fairy+=1
            elif t.typing=="Water":
                i.steel+=1
                i.fire+=1
                i.water+=1
                i.grass+=-1
                i.electric+=-1
                i.ice+=1
        for t in typing:
            if t.typing=="Dark":
                i.psychic=3
            elif t.typing=="Fairy":
                i.dragon=3
            elif t.typing=="Flying":
                i.ground=3
            elif t.typing=="Ghost":
                i.normal=3
                i.fighting=3
            elif t.typing=="Ground":
                i.electric=3
            elif t.typing=="Normal":
                i.ghost=3
            elif t.typing=="Steel":
                i.poison=3
        i.save()
        j+=1
    return redirect('home')