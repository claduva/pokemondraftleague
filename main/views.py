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
from draftplanner.models import *
from .forms import HelpForm

from replayanalysis.NewParser.parser import *
from replayanalysis.models import *
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
    target={}
    target['nickname']=""
    target['pokemon']=""
    attacker={}
    attacker['nickname']=""
    attacker['pokemon']=""
    move=""
    moveswithsecondaryeffect=dict([['Fire Punch', 10], ['Zing Zap', 30], ['Ice Punch', 10], ['Thunder Shock', 10], ['Poison Sting', 30], ['Focus Blast', 10], ['Liquidation', 20], ['Crush Claw', 50], ['Metal Claw', 10], ['Acid', 10], ['Aurora Beam', 10], ['Heart Stamp', 30], ['Crunch', 20], ['Water Pulse', 20], ['Thunder Punch', 10], ['Extrasensory', 10], ['Blizzard', 10], ['Paleo Wave', 20], ['Freeze-Dry', 10], ['Dizzy Punch', 20], ['Signal Beam', 10], ['Steamroller', 30], ['Astonish', 30], ['Energy Ball', 10], ['Iron Tail', 30], ['Charge Beam', 70], ['Secret Power', 30], ['Tri Attack', 20], ['Psychic', 10], ['Smog', 40], ['Steel Wing', 10], ['Iron Head', 30], ['Headbutt', 30], ['Bug Buzz', 10], ['Sludge', 30], ['Mist Ball', 50], ['Earth Power', 10], ['Bolt Strike', 20], ['Bite', 30], ['Rock Climb', 20], ['Freeze Shock', 30], ['Dark Pulse', 20], ['Flash Cannon', 10], ['Floaty Fall', 30], ['Poison Fang', 50], ['Sludge Bomb', 30], ['Lick', 30], ['Shadow Ball', 20], ['Cross Poison', 10], ['Sludge Wave', 10], ['Leaf Tornado', 50], ['Hyper Fang', 10], ['Thunder', 30], ['Constrict', 10], ['Stomp', 30], ['Poison Tail', 10], ['Bone Club', 10], ['Fire Blast', 10], ['Mud Bomb', 30], ['Twineedle', 20], ['Splishy Splash', 30], ['Confusion', 10], ['Fiery Dance', 50], ['Night Daze', 40], ['Flare Blitz', 10], ['Sacred Fire', 50], ['Ice Beam', 10], ['Poison Jab', 30], ['Double Iron Bash', 30], ['Waterfall', 20], ['Psybeam', 10], ['Octazooka', 50], ['Spark', 30], ['Mirror Shot', 30], ['Dragon Rush', 20], ['Luster Purge', 50], ['Snore', 30], ['Thunderbolt', 10], ['Flame Wheel', 10], ['Bounce', 30], ['Scald', 30], ['Force Palm', 30], ['Hurricane', 30], ['Ice Burn', 30], ['Gunk Shot', 30], ['Blaze Kick', 10], ['Searing Shot', 30], ['Twister', 20], ['Bubble', 10], ['Rock Smash', 50], ['Volt Tackle', 10], ['Ember', 10], ['Powder Snow', 10], ['Moonblast', 30], ['Rock Slide', 30], ['Heat Wave', 10], ['Discharge', 30], ['Razor Shell', 50], ['Rolling Kick', 30], ['Blue Flare', 20], ['Sky Attack', 30], ['Relic Song', 10], ['Ancient Power', 10], ['Bubble Beam', 10], ['Play Rough', 10], ['Zen Headbutt', 20], ['Shadow Strike', 50], ['Body Slam', 30], ['Seed Flare', 40], ['Flamethrower', 10], ['Diamond Storm', 50], ['Muddy Water', 30], ['Steam Eruption', 30], ['Needle Arm', 30], ['Dragon Breath', 30], ['Silver Wind', 10], ['Air Slash', 30], ['Lava Plume', 30], ['Meteor Mash', 20], ['Icicle Crash', 30], ['Shadow Bone', 20], ['Ominous Wind', 10], ['Strange Steam', 20], ['Pyro Ball', 10]])
    moveswithsecondaryeffect1=dict([
    ['Thunder Punch', ['status', 'par',target['nickname'],.1,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Fire Punch', ['status', 'brn',target['nickname'],.1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Fire Fang', ['status', 'brn',target['nickname'],.1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Pyro Ball', ['status', 'brn',target['nickname'],.1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Zing Zap', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Extrasensory', ['cant', 'flinch',target['nickname'], .1,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Ice Punch', ['status', 'frz',target['nickname'], .1,f"{target['pokemon']} was frozen by {attacker['pokemon']} with {move}"]], 
    ['Ice Fang', ['status', 'frz',target['nickname'], .1,f"{target['pokemon']} was frozen by {attacker['pokemon']} with {move}"]], 
    ['Thunder Fang', ['status', 'par',target['nickname'],.1,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Thunder Shock', ['status', 'par',target['nickname'],.1,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Poison Sting', ['status', 'psn',target['nickname'], .3,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Focus Blast', ['unboost', 'spd|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Liquidation', ['unboost', 'def|1',target['nickname'], .2,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Crush Claw', ['unboost', 'def|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Metal Claw', ['boost', 'atk|1 ',attacker['nickname'], .1,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Acid', ['unboost', 'spd|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Aurora Beam', ['unboost', 'atk|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Heart Stamp', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Crunch', ['unboost', 'def|1',target['nickname'], .2,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Water Pulse', ['start', 'confusion',target['nickname'], .2,f"{target['pokemon']} was confused by {attacker['pokemon']} with {move}"]], 
    ['Blizzard', ['status', 'frz',target['nickname'], .1,f"{target['pokemon']} was frozen by {attacker['pokemon']} with {move}"]], 
    ['Paleo Wave', ['unboost', 'atk|1',target['nickname'], .2,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Freeze-Dry', ['status', 'frz',target['nickname'], .1,f"{target['pokemon']} was frozen by {attacker['pokemon']} with {move}"]], 
    ['Dizzy Punch', ['start', 'confusion',target['nickname'], .2,f"{target['pokemon']} was confused by {attacker['pokemon']} with {move}"]], 
    ['Relic Song', ['status', 'slp',target['nickname'], .1,f"{target['pokemon']} was put to sleep by {attacker['pokemon']} with {move}"]], 
    ['Signal Beam', ['start', 'confusion',target['nickname'], .1,f"{target['pokemon']} was confused by {attacker['pokemon']} with {move}"]], 
    ['Ancient Power', ['boost', 'atk|1',target['nickname'], .1,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Steamroller', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Bubble Beam', ['unboost', 'spe|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Sludge', ['status', 'psn',target['nickname'], .3,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Play Rough', ['unboost', 'atk|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Astonish', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Energy Ball', ['unboost', 'spd|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Zen Headbutt', ['cant', 'flinch',target['nickname'], .2,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Iron Tail', ['unboost', 'def|1',target['nickname'], .3,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Shadow Strike', ['unboost', 'def|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Charge Beam', ['boost', 'spa|1',target['nickname'], .7,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Secret Power', ['status', 'par',target['nickname'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Tri Attack', ['status', '',target['nickname'],.2,f"{target['pokemon']} was statused by {attacker['pokemon']} with {move}"]], 
    ['Psychic', ['unboost', 'spd|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Smog', ['status', 'psn',target['nickname'],.4,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Steel Wing', ['boost', 'def|1',target['nickname'], .1,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Iron Head', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Headbutt', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Body Slam', ['status', 'par',target['nickname'],.3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Bug Buzz', ['unboost', 'spd|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Seed Flare', ['unboost', 'spd|2',target['nickname'], .4,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Mist Ball', ['unboost', 'spa|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Earth Power', ['unboost', 'spd|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Bolt Strike', ['status', 'par',target['nickname'], .2,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Bite', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Flamethrower', ['status', 'brn',target['nickname'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Rock Climb', ['start', 'confusion',target['nickname'], .2,f"{target['pokemon']} was confused by {attacker['pokemon']} with {move}"]], 
    ['Freeze Shock', ['status', 'par',target['nickname'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Dark Pulse', ['cant', 'flinch',target['nickname'], .2,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Flash Cannon', ['unboost', 'spd|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Floaty Fall', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Poison Fang', ['status', 'tox',target['nickname'], .5,f"{target['pokemon']} was toxiced by {attacker['pokemon']} with {move}"]], 
    ['Sludge Bomb', ['status', 'psn',target['nickname'], .3,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Lick', ['status','par',target['nickname'],.3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Diamond Storm', ['boost', 'def|2',target['nickname'], .5,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Shadow Ball', ['unboost', 'spd|1',target['nickname'], .2,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Cross Poison', ['status', 'psn',target['nickname'], .1,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Sludge Wave', ['status', 'psn',target['nickname'], .1,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Leaf Tornado', ['unboost', 'accuracy|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Hyper Fang', ['cant', 'flinch',target['nickname'], .1,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Muddy Water', ['unboost', 'accuracy|1',target['nickname'], .3,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Thunder', ['status', 'par',target['nickname'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Constrict', ['unboost', 'spe|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Stomp', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Poison Tail', ['status', 'psn',target['nickname'], .1,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Bone Club', ['cant', 'flinch',target['nickname'], .1,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Fire Blast', ['status', 'brn',target['nickname'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Mud Bomb', ['unboost', 'accuracy|1',target['nickname'], .3,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Twineedle', ['status', 'psn',target['nickname'],.2,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Splishy Splash', ['status', 'par',target['nickname'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Confusion', ['start', 'confusion',target['nickname'], .1,f"{target['pokemon']} was confused by {attacker['pokemon']} with {move}"]], 
    ['Steam Eruption', ['status', 'brn',target['nickname'], .3,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Fiery Dance', ['boost', 'spa|1',target['nickname'], .5,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Night Daze', ['unboost', 'accuracy|1',target['nickname'], .4,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Flare Blitz', ['status', 'brn',target['nickname'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Mirror Shot', ['unboost', 'accuracy|1',target['nickname'], .3,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Sacred Fire', ['status', 'brn',target['nickname'], .5,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Ice Beam', ['status', 'frz',target['nickname'], .1,f"{target['pokemon']} was frozen by {attacker['pokemon']} with {move}"]], 
    ['Poison Jab', ['status', 'psn',target['nickname'], .3,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Double Iron Bash', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Waterfall', ['cant', 'flinch',target['nickname'], .2,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Psybeam', ['start', 'confusion',target['nickname'], .1,f"{target['pokemon']} was confused by {attacker['pokemon']} with {move}"]], 
    ['Strange Steam', ['start', 'confusion',target['nickname'], .2,f"{target['pokemon']} was confused by {attacker['pokemon']} with {move}"]], 
    ['Octazooka', ['unboost', 'accuracy|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Spark', ['status', 'par',target['nickname'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Needle Arm', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Dragon Breath', ['status', 'par',target['nickname'],.3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Air Slash', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Dragon Rush', ['cant', 'flinch',target['nickname'], .2,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Silver Wind', ['boost', 'atk|1',target['nickname'], .1,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Luster Purge', ['unboost', 'spd|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Snore', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Thunderbolt', ['status', 'par',target['nickname'], .1,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Flame Wheel', ['status', 'brn',target['nickname'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Bounce', ['status', 'par',target['nickname'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Scald', ['status', 'brn',target['nickname'], .3,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Force Palm', ['status', 'par',target['nickname'],.3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Hurricane', ['start', 'confusion',target['nickname'], .3,f"{target['pokemon']} was confused by {attacker['pokemon']} with {move}"]], 
    ['Ice Burn', ['status', 'brn',target['nickname'], .3,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Gunk Shot', ['status', 'psn',target['nickname'], .3,f"{target['pokemon']} was poisoned by {attacker['pokemon']} with {move}"]], 
    ['Blaze Kick', ['status', 'brn',target['nickname'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Lava Plume', ['status', 'brn',target['nickname'], .3,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Meteor Mash', ['boost', 'atk|1',target['nickname'], .2,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Searing Shot', ['status', 'brn',target['nickname'], .3,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Twister', ['cant', 'flinch',target['nickname'], .2,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Icicle Crash', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Bubble', ['unboost', 'spe|1',target['nickname'], .1,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Rock Smash', ['unboost', 'def|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Volt Tackle', ['status', 'par',target['nickname'], .1,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Ember', ['status', 'brn',target['nickname'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Powder Snow', ['status', 'frz',target['nickname'], .1,f"{target['pokemon']} was frozen by {attacker['pokemon']} with {move}"]], 
    ['Moonblast', ['unboost', 'spa|1',target['nickname'], .3,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Rock Slide', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Shadow Bone', ['unboost', 'def|1',target['nickname'], .2,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Heat Wave', ['status', 'brn',target['nickname'], .1,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Discharge', ['status', 'par',target['nickname'], .3,f"{target['pokemon']} was paralyzed by {attacker['pokemon']} with {move}"]], 
    ['Ominous Wind', ['boost', 'atk|1',target['nickname'], .1,f"{attacker['pokemon']} received a stat boost as a secondary effect from {move}"]], 
    ['Razor Shell', ['unboost', 'def|1',target['nickname'], .5,f"{target['pokemon']} suffered a stat drop via secondary effect by {attacker['pokemon']} with {move}"]], 
    ['Rolling Kick', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]], 
    ['Blue Flare', ['status', 'brn',target['nickname'], .2,f"{target['pokemon']} was burned by {attacker['pokemon']} with {move}"]], 
    ['Sky Attack', ['cant', 'flinch',target['nickname'], .3,f"{target['pokemon']} was flinched by {attacker['pokemon']} with {move}"]]])
    for move in moveswithsecondaryeffect.keys():
        if move not in moveswithsecondaryeffect1.keys():
            print(move)
    return redirect('home')

def get_pkmn(pkmn):
    try:
        pkmn=all_pokemon.objects.get(pokemon=pkmn)
    except:
        #adjust
        pkmn=pkmn.replace(" (Alola)","-Alola").replace(" (Dusk)","-Dusk").replace(" (Day)","").replace("-Day","").replace(". ",".").replace(" (BB)","-Ash").replace("-I","").replace("-E","-Eternal")
        pkmn=pkmn.replace("Blue ","").replace("-T","-Therian").replace("-O","-o").replace(" 50%","").replace(" 10%","-10%")
        pkmn=pkmn.replace("Cryoganol","Cryogonal").replace("Cincinno","Cinccino")
        if pkmn.find("M.")>-1:
            pkmn=pkmn.replace("M.","")+"-Mega"
        if pkmn.find("M-")>-1:
            pkmn=pkmn.replace("M-","")+"-Mega"
        if pkmn.find("A-")>-1:
            pkmn=pkmn.replace("A-","")+"-Alola"
        if pkmn.find("Alolan ")>-1:
            pkmn=pkmn.replace("Alolan ","")+"-Alola"
        if pkmn.find("Alola ")>-1:
            pkmn=pkmn.replace("Alola ","")+"-Alola"
        if pkmn.find("Mega ")>-1:
            pkmn=pkmn.replace("Mega ","")+"-Mega"
        try:
            pkmn=all_pokemon.objects.get(pokemon=pkmn)
        except:
            print(pkmn)
            #raise
    return pkmn