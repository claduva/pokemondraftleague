from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
from django.db.models import Q
from django.core.files.base import ContentFile
from django.template import Context, loader
from django.contrib.sessions.models import Session
from django.utils import timezone

import json
from datetime import datetime
import time
import csv
import os
import requests
import math
import sys, traceback
from background_task import background

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
            online=None
            context = {
                "title": "Pokemon Draft League",
                "yourleagues": yourleagues,
                "upcomingmatches":upcomingmatches,
                "recentresults": recentresults,
                "online":online,
            }
            return  render(request,"coachlandingpage.html", context)
    except Exception as e:
        pass
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
    return render(request,"404.html")

def custom500(request):
    type_, value, traceback_ = sys.exc_info()
    context={'exception':value}
    return render(request,"500.html",context)

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

def moveleaderboard(request):
    leaderboard=moveinfo.objects.all().filter(uses__gt=0).order_by('-uses')
    context = {
        "leaderboard": leaderboard
    }
    return  render(request,"moveleaderboard.html",context)

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
    """
    monstoadd=all_pokemon.objects.all().filter(Q(pokemon__contains="-Gmax")|Q(pokemon__contains="-Galar")|Q(pokemon__contains="Zarude")|Q(pokemon__contains="Kubfu")|Q(pokemon__contains="-Urshifu"))
    templates=pokemon_tier.objects.all().order_by('subleague').distinct('subleague')
    for t in templates:
        bannedtier=leaguetiers.objects.filter(subleague=t.subleague).get(tiername="Banned")
        for p in monstoadd:
            try:
                id_=pokemon_tier.objects.all().order_by('-id').first().id+1
                pokemon_tier.objects.create(id=id_,pokemon=p,league=t.league,subleague=t.subleague,tier=bannedtier)
            except Exception as e:
                print(e)
    """
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

def updatelearnsets(request): 
    learnset_update()
    return redirect('home')

@check_if_clad
def start_tasks(request): 
    print("Starting delete unused models")
    delete_unused_models(schedule=60,repeat=60*60*24,repeat_until=None)
    print("Starting run pickems")
    run_pickems(schedule=60*2,repeat=60*60,repeat_until=None)
    print("Starting execute free agency and trades")
    execute_free_agency_and_trades(schedule=60*3,repeat=60*15,repeat_until=None)
    print("Starting pokemon stat update")
    pokemon_stat_update(schedule=60*5,repeat=60*60,repeat_until=None)
    print("Starting award check")
    award_check(schedule=60*20,repeat=60*60,repeat_until=None)
    print("Starting user stat update")
    user_stat_update(schedule=60*35,repeat=60*60,repeat_until=None)
    print("Starting run replay database")
    run_replay_database(schedule=60*50,repeat=60*60,repeat_until=None)
    return redirect('home')

##--------------------------------------------TASKS--------------------------------------------
@background(schedule=1)
def delete_unused_models():
    print("**************************************************")
    print("TASK: Running delete unused models")
    print("**************************************************")
    for item in league.objects.all():  
        diff=abs((item.created.replace(tzinfo=None)-datetime.now()).days)
        if diff>7:
            numhist=historical_team.objects.all().filter(league=item).count()
            if numhist==0:
                try: 
                    conf=item.configuration
                except:
                    item.delete()

@background(schedule=1)
def run_replay_database():
  print("**************************************************")
  print("TASK: Running replay databae")
  print("**************************************************")
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
      if match.match_replay.data['team1']['wins']==1:
        j=match.match_replay.data['team1']['coach']
      elif match.match_replay.data['team2']['wins']==1:
        j=match.match_replay.data['team2']['coach']
      else:
        j="N/A"
    except:
      g="N/A"
      h="N/A"
      j="N/A"
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
      databaseitem.winneruser=j
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
        winneruser=j,
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
      if match.historical_match_replay.data['team1']['wins']==1:
        j=match.historical_match_replay.data['team1']['coach']
      elif match.historical_match_replay.data['team2']['wins']==1:
        j=match.historical_match_replay.data['team2']['coach']
      else:
        j="N/A"
    except:
      g="N/A"
      h="N/A"
      j="N/A"
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
      databaseitem.winneruser=j
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
        winneruser=j,
        replay=i,
      )
    print(f'{counter}/{total}')
    counter+=1

@background(schedule=1)
def user_stat_update():
    print("**************************************************")
    print("TASK: Running user stat update")
    print("**************************************************")
    allusers=User.objects.all()
    for userofinterest in allusers:
        try:
            userprofile=userofinterest.profile
        except:
            userprofile=profile.objects.create(user=userofinterest)
        userprofile.wins=0
        userprofile.losses=0
        userprofile.seasonsplayed=0
        userprofile.differential=0
        userprofile.playoffwins=0
        userprofile.playofflosses=0
        userprofile.seasonsplayed=0
        userprofile.playoffdifferential=0
        userprofile.support=0
        userprofile.damagedone=0
        userprofile.hphealed=0
        userprofile.luck =0
        userprofile.remaininghealth=0
        userprofile.save()
        coaching=coachdata.objects.filter(Q(coach=userofinterest)|Q(teammate=userofinterest)).exclude(league_name__name__icontains="Test")
        for item in coaching:
            userprofile.support+=item.support
            userprofile.damagedone+=item.damagedone
            userprofile.hphealed+=item.hphealed
            userprofile.luck+=item.luck
            userprofile.remaininghealth+=item.remaininghealth
        priorseasons=historical_team.objects.filter(Q(coach1=userofinterest)|Q(coach2=userofinterest)).exclude(league__name__icontains="Test")
        for item in priorseasons:
            userprofile.support+=item.support
            userprofile.damagedone+=item.damagedone
            userprofile.hphealed+=item.hphealed
            userprofile.luck+=item.luck
            userprofile.remaininghealth+=item.remaininghealth
        alternativeseasoncount=schedule.objects.all().filter(Q(team1alternateattribution=userofinterest)|Q(team2alternateattribution=userofinterest)).distinct('season').count()+historical_match.objects.all().filter(Q(team1alternateattribution=userofinterest)|Q(team2alternateattribution=userofinterest)).distinct('team1__seasonname').count()
        seasonsplayed=coaching.count()+priorseasons.count()+alternativeseasoncount
        usermatches=replaydatabase.objects.all().filter(Q(team1coach1=userofinterest)|Q(team1coach2=userofinterest)|Q(team2coach1=userofinterest)|Q(team2coach2=userofinterest))
        wins=usermatches.filter(Q(winnercoach1=userofinterest)|Q(winnercoach2=userofinterest))
        playoffusermatches=usermatches.filter(Q(associatedmatch__week__icontains="Playoff")|Q(associatedhistoricmatch__week__icontains="Playoff"))
        playoffwins=playoffusermatches.filter(Q(winnercoach1=userofinterest)|Q(winnercoach2=userofinterest))
        for item in usermatches:
            if userofinterest==item.winnercoach1 or userofinterest==item.winnercoach1:
                if item.associatedmatch != None:
                    userprofile.differential+=max(item.associatedmatch.team1score,item.associatedmatch.team2score)
                elif item.associatedhistoricmatch != None:
                    userprofile.differential+=max(item.associatedhistoricmatch.team1score,item.associatedhistoricmatch.team2score)
            else:
                if item.associatedmatch != None:
                    userprofile.differential+=-max(item.associatedmatch.team1score,item.associatedmatch.team2score)
                elif item.associatedhistoricmatch != None:
                    userprofile.differential+=-max(item.associatedhistoricmatch.team1score,item.associatedhistoricmatch.team2score)
        for item in playoffusermatches:            
            if userofinterest==item.winnercoach1 or userofinterest==item.winnercoach1:
                if item.associatedmatch != None:
                    userprofile.playoffdifferential+=max(item.associatedmatch.team1score,item.associatedmatch.team2score)
                elif item.associatedhistoricmatch != None:
                    userprofile.playoffdifferential+=max(item.associatedhistoricmatch.team1score,item.associatedhistoricmatch.team2score)
            else:
                if item.associatedmatch != None:
                    userprofile.playoffdifferential+=-max(item.associatedmatch.team1score,item.associatedmatch.team2score)
                elif item.associatedhistoricmatch != None:
                    userprofile.playoffdifferential+=-max(item.associatedhistoricmatch.team1score,item.associatedhistoricmatch.team2score)
        userprofile.wins+=wins.count()
        userprofile.losses+=usermatches.count()-wins.count()
        userprofile.playoffwins+=playoffwins.count()
        userprofile.playofflosses+=playoffusermatches.count()-playoffwins.count()
        userprofile.seasonsplayed=seasonsplayed
        userprofile.save()

@background(schedule=1)
def award_check():
    print("**************************************************")
    print("TASK: Running award check")
    print("**************************************************")
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
                finalsmatch=schedule.objects.all().filter(season=s,season__league=item).exclude(winner__isnull=True).get(week="Playoffs Finals")
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
                pass
            #check third place
            try:
                awardtogive=award.objects.get(awardname="Thirdplace")
                thirdplacematch=schedule.objects.all().filter(season=s,season__league=item).exclude(winner__isnull=True).get(week="Playoffs Third Place Match")
                winner=thirdplacematch.winner
                messagebody=f'Congratulations! You have been awarded a trophy for coming in third place in a season. Check it out at https://www.pokemondraftleague.online/users/{winner.coach.username}'
                awardcheck(winner.coach,awardtogive,awardtext,messagebody,admin)
                if winner.teammate != None:
                    messagebody=f'Congratulations! You have been awarded a trophy for coming in third place in a season. Check it out at https://www.pokemondraftleague.online/users/{winner.teammate.username}'
                    awardcheck(winner.teammate,awardtogive,awardtext,messagebody,admin)
            except:
                pass
            ##check playoffs
            awardtogive=award.objects.get(awardname="Playoffs")
            season_playoffmatches=schedule.objects.all().filter(season=s,season__league=item,week__contains="Playoffs").exclude(winner__isnull=True).distinct('winner')
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
                finalsmatch=historical_match.objects.all().filter(team1__league=item,team1__seasonname=s.seasonname).exclude(winner__isnull=True).get(week="Playoffs Finals")
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
                pass
            #check third place
            try:
                awardtogive=award.objects.get(awardname="Thirdplace")
                thirdplacematch=historical_match.objects.all().filter(team1__league=item,team1__seasonname=s.seasonname).exclude(winner__isnull=True).get(week="Playoffs Third Place Match")
                winner=thirdplacematch.winner
                messagebody=f'Congratulations! You have been awarded a trophy for coming in third place in a season. Check it out at https://www.pokemondraftleague.online/users/{winner.coach1.username}'
                awardcheck(winner.coach1,awardtogive,awardtext,messagebody,admin)
                if winner.coach2 != None:
                    messagebody=f'Congratulations! You have been awarded a trophy for coming in third place in a season. Check it out at https://www.pokemondraftleague.online/users/{winner.coach2.username}'
                    awardcheck(winner.coach2,awardtogive,awardtext,messagebody,admin)
            except:
                pass
            ##check playoffs
            awardtogive=award.objects.get(awardname="Playoffs")
            season_playoffmatches=historical_match.objects.all().filter(team1__league=item,team1__seasonname=s.seasonname,week__contains="Playoffs").exclude(winner__isnull=True).distinct('winner')
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
        try:
            prof=u.profile
        except:
            prof=profile.objects.create(user=u)
        seasoncount=prof.seasonsplayed
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

@background(schedule=1)
def execute_free_agency_and_trades():
  print("**************************************************")
  print("TASK: Running execute free agency and trades")
  print("**************************************************")
  #free agencies
  unexecutedfa=free_agency.objects.all().filter(executed=False).order_by('id')
  #check if completed matches
  for item in unexecutedfa:
    request_league=seasonsetting.objects.get(subleague=item.season.subleague)
    requestedweek=item.weekeffective
    completedmatches=True
    if requestedweek >=2:
      for i in range(1,requestedweek):
        try:
          matchofinterest=schedule.objects.filter(season=item.season).filter(Q(team1=item.coach)|Q(team2=item.coach)).get(week=str(i))
          if matchofinterest.replay=="Link":
            completedmatches=False
        except:
          print('Match not found')
    if completedmatches:
      #execute free agencies
      montoupdate=item.droppedpokemon
      try:
        droppedpokemon=roster.objects.filter(season=item.season,team=item.coach).get(pokemon=item.droppedpokemon)
        item.executed=True
        montoupdate.kills=droppedpokemon.kills
        droppedpokemon.kills=0
        montoupdate.deaths=droppedpokemon.deaths
        droppedpokemon.deaths=0
        montoupdate.gp=droppedpokemon.gp
        droppedpokemon.gp=0
        montoupdate.gw=droppedpokemon.gw
        droppedpokemon.gw=0
        montoupdate.differential=droppedpokemon.differential
        droppedpokemon.differential=0
        montoupdate.support=droppedpokemon.support
        droppedpokemon.support=0
        montoupdate.hphealed=droppedpokemon.hphealed
        droppedpokemon.hphealed=0
        montoupdate.luck=droppedpokemon.luck
        droppedpokemon.luck=0
        montoupdate.damagedone=droppedpokemon.damagedone
        droppedpokemon.damagedone=0
        montoupdate.remaininghealth=droppedpokemon.remaininghealth
        droppedpokemon.remaininghealth=0
        droppedpokemon.zuser="N"     
        droppedpokemon.pokemon=item.addedpokemon
      except:
        try:
          droppedpokemon=roster.objects.filter(season=item.season,team=item.coach).get(pokemon=item.addedpokemon)
          item.executed=True
          montoupdate.kills=droppedpokemon.kills
          droppedpokemon.kills=0
          montoupdate.deaths=droppedpokemon.deaths
          droppedpokemon.deaths=0
          montoupdate.gp=droppedpokemon.gp
          droppedpokemon.gp=0
          montoupdate.gw=droppedpokemon.gw
          droppedpokemon.gw=0
          montoupdate.differential=droppedpokemon.differential
          droppedpokemon.differential=0
          montoupdate.support=droppedpokemon.support
          droppedpokemon.support=0
          montoupdate.hphealed=droppedpokemon.hphealed
          droppedpokemon.hphealed=0
          montoupdate.luck=droppedpokemon.luck
          droppedpokemon.luck=0
          montoupdate.damagedone=droppedpokemon.damagedone
          droppedpokemon.damagedone=0
          montoupdate.remaininghealth=droppedpokemon.remaininghealth
          droppedpokemon.remaininghealth=0
          droppedpokemon.zuser="N"  
        except:
          pass
      item.save()
      droppedpokemon.save() 
      montoupdate.save()
  #trades
  unexecutedtrades=trading.objects.all().filter(executed=False).order_by('id')
  print(unexecutedtrades)
  #check if completed matches
  for item in unexecutedtrades:
    request_league=seasonsetting.objects.get(subleague=item.season.subleague)
    requestedweek=item.weekeffective
    completedmatches=True
    if requestedweek >= 2:
      for i in range(1,requestedweek):
        try:
          matchofinterest=schedule.objects.filter(season=item.season).filter(Q(team1=item.coach)|Q(team2=item.coach)).get(week=str(i))
          if matchofinterest.replay=="Link":
            completedmatches=False
        except:
          print('Match not found')
    if completedmatches:
      #execute trades
      montoupdate=item.droppedpokemon
      try:
        droppedpokemon=roster.objects.filter(season=item.season,team=item.coach).get(pokemon=item.droppedpokemon)
        montoupdate.kills=droppedpokemon.kills
        droppedpokemon.kills=0
        montoupdate.deaths=droppedpokemon.deaths
        droppedpokemon.deaths=0
        montoupdate.gp=droppedpokemon.gp
        droppedpokemon.gp=0
        montoupdate.gw=droppedpokemon.gw
        droppedpokemon.gw=0
        montoupdate.differential=droppedpokemon.differential
        droppedpokemon.differential=0
        montoupdate.support=droppedpokemon.support
        droppedpokemon.support=0
        montoupdate.hphealed=droppedpokemon.hphealed
        droppedpokemon.hphealed=0
        montoupdate.luck=droppedpokemon.luck
        droppedpokemon.luck=0
        montoupdate.damagedone=droppedpokemon.damagedone
        droppedpokemon.damagedone=0
        montoupdate.remaininghealth=droppedpokemon.remaininghealth
        droppedpokemon.remaininghealth=0
        droppedpokemon.zuser="N"
        droppedpokemon.pokemon=item.addedpokemon
        item.executed=True
      except:
        try:
          droppedpokemon=roster.objects.filter(season=item.season,team=item.coach).get(pokemon=item.droppedpokemon)
          montoupdate.kills=droppedpokemon.kills
          droppedpokemon.kills=0
          montoupdate.deaths=droppedpokemon.deaths
          droppedpokemon.deaths=0
          montoupdate.gp=droppedpokemon.gp
          droppedpokemon.gp=0
          montoupdate.gw=droppedpokemon.gw
          droppedpokemon.gw=0
          montoupdate.differential=droppedpokemon.differential
          droppedpokemon.differential=0
          montoupdate.support=droppedpokemon.support
          droppedpokemon.support=0
          montoupdate.hphealed=droppedpokemon.hphealed
          droppedpokemon.hphealed=0
          montoupdate.luck=droppedpokemon.luck
          droppedpokemon.luck=0
          montoupdate.damagedone=droppedpokemon.damagedone
          droppedpokemon.damagedone=0
          montoupdate.remaininghealth=droppedpokemon.remaininghealth
          droppedpokemon.remaininghealth=0
          droppedpokemon.zuser="N"
          item.executed=True
        except:
          pass
      item.save()
      droppedpokemon.save() 
      montoupdate.save()

@background(schedule=1)
def run_pickems():
  print("**************************************************")
  print("TASK: Running pickems")
  print("**************************************************")
  """
  leaderboard=pickem_leaderboard.objects.all()
  for item in leaderboard:
      item.submitted=0
      item.numbercorrect=0
      item.matchescompleted=0
      item.save()
      pickemlist=item.user.pickems.all()
      for p in pickemlist:
          item.submitted+=1
          if p.match.replay != "Link":
              item.matchescompleted+=1
              if p.pick==p.match.winner:
                  item.numbercorrect+=1
      item.save()
  """

@background(schedule=1)
def pokemon_stat_update():
    print("**************************************************")
    print("TASK: Running pokemon stat update")
    print("**************************************************")
    leaderboard=pokemon_leaderboard.objects.all()
    for item in leaderboard:
        #set baseline
        item.kills=item.pokemon.kills
        item.deaths=item.pokemon.deaths
        item.differential = item.pokemon.differential
        item.gp=item.pokemon.gp
        item.gw=item.pokemon.gw
        item.timesdrafted=0 
        item.support=item.pokemon.support
        item.damagedone=item.pokemon.damagedone
        item.hphealed=item.pokemon.hphealed
        item.luck =item.pokemon.luck
        item.remaininghealth=item.pokemon.remaininghealth
        item.save()
        #update based on rosters
        rosterson=item.pokemon.pokemonroster.all()
        for team in rosterson:
            if team.season.league.name.find('Test')==-1:
                item.kills+=team.kills
                item.deaths+=team.deaths
                item.differential+=team.differential
                item.gp+=team.gp
                item.gw+=team.gw
                item.support+=team.support
                item.damagedone+=team.damagedone
                item.hphealed+=team.hphealed
                item.luck+=team.luck
                item.remaininghealth+=team.remaininghealth
        historicrosterson=item.pokemon.historicalpokemonroster.all()
        for team in historicrosterson:
            if team.team.league.name.find('Test')==-1:
                item.kills+=team.kills
                item.deaths+=team.deaths
                item.differential+=team.differential
                item.gp+=team.gp
                item.gw+=team.gw
                item.support+=team.support
                item.damagedone+=team.damagedone
                item.hphealed+=team.hphealed
                item.luck+=team.luck
                item.remaininghealth+=team.remaininghealth
        item.timesdrafted=item.pokemon.historicalpokemondraft.all().count()+item.pokemon.pokemondraft.all().count()
        item.save()

@background(schedule=1)
def learnset_update():
    print("**************************************************")
    print("TASK: Running learnset update")
    print("**************************************************")
    pokemon_moveset.objects.all().delete()
    allmoves=moveinfo.objects.all()
    with open('learnsets.json') as json_file:
        data = json.load(json_file)
        id_=1
        for item in all_pokemon.objects.all():
            print(f'{id_}: {item.pokemon}')
            id_+=1
            name=item.pokemon.lower().replace("-mega-x","").replace("-mega-y","").replace("-mega","").replace("-gmax","").replace(" ","").replace("-","").replace("-y","").replace("-x","").replace(".","").replace(":","").replace("unbound","").replace("primal","").replace("therian","").replace("shayminsky","shaymin")
            name=name.replace('deoxysattack','deoxys').replace('deoxysdefense','deoxys').replace('deoxysspeed','deoxys').replace('origin','').replace('10%','').replace('complete','').replace('wormadamtrash','wormadam').replace('wormadamsandy','wormadam').replace('indeedeef','indeedee').replace('meowsticf','meowstic')
            try:
                ls=data[name]['learnset']
                for move in ls:
                    try:
                        moi=allmoves.get(altname=move)
                    except:
                        print(move)
                    try:
                        try:
                            idd=pokemon_moveset.objects.all().order_by('-id').first().id+1
                        except:
                            idd=1
                        pokemon_moveset.objects.create(id=idd,pokemon=item,moveinfo=moi)
                    except:
                        pass
            except:
                pass
    for item in preevolution.objects.all():
        monsmoveset=list(item.pokemon.moves.all().values_list('moveinfo__id',flat=True))
        movestoadd=item.preevo.moves.all().exclude(moveinfo__id__in=monsmoveset)
        for item_ in movestoadd:
            id_=pokemon_moveset.objects.all().order_by('-id').first().id+1
            try:
                pokemon_moveset.objects.create(id=id_,pokemon=item.pokemon,moveinfo=item_.moveinfo)
            except:
                pass
    for item in all_pokemon.objects.all().filter(pokemon__contains="-Gmax"):
        monsmoveset=list(item.moves.all().values_list('moveinfo__id',flat=True))
        basemon=all_pokemon.objects.get(pokemon=item.pokemon.replace("-Gmax",""))
        movestoadd=basemon.moves.all().exclude(moveinfo__id__in=monsmoveset)
        for item_ in movestoadd:
            id_=pokemon_moveset.objects.all().order_by('-id').first().id+1
            try:
                pokemon_moveset.objects.create(id=id_,pokemon=item,moveinfo=item_.moveinfo)
            except Exception as e:
                pass
    for item in all_pokemon.objects.all().filter(pokemon__contains="-Mega"):
        monsmoveset=list(item.moves.all().values_list('moveinfo__id',flat=True))
        basemon=all_pokemon.objects.get(pokemon=item.pokemon.replace("-Mega-X","").replace("-Mega-Y","").replace("-Mega",""))
        movestoadd=basemon.moves.all().exclude(moveinfo__id__in=monsmoveset)
        for item_ in movestoadd:
            id_=pokemon_moveset.objects.all().order_by('-id').first().id+1
            try:
                pokemon_moveset.objects.create(id=id_,pokemon=item,moveinfo=item_.moveinfo)
            except Exception as e:
                pass
    for item in all_pokemon.objects.all().filter(pokemon__contains="-Crowned"):
        monsmoveset=list(item.moves.all().values_list('moveinfo__id',flat=True))
        basemon=all_pokemon.objects.get(pokemon=item.pokemon.replace("-Crowned",""))
        movestoadd=basemon.moves.all().exclude(moveinfo__id__in=monsmoveset)
        for item_ in movestoadd:
            id_=pokemon_moveset.objects.all().order_by('-id').first().id+1
            try:
                pokemon_moveset.objects.create(id=id_,pokemon=item,moveinfo=item_.moveinfo)
            except Exception as e:
                pass
    for item in all_pokemon.objects.all().filter(pokemon__contains="Rotom").exclude(pokemon="Rotom"):
        monsmoveset=list(item.moves.all().values_list('moveinfo__id',flat=True))
        basemon=all_pokemon.objects.get(pokemon="Rotom")
        movestoadd=basemon.moves.all().exclude(moveinfo__id__in=monsmoveset)
        for item_ in movestoadd:
            id_=pokemon_moveset.objects.all().order_by('-id').first().id+1
            try:
                pokemon_moveset.objects.create(id=id_,pokemon=item,moveinfo=item_.moveinfo)
            except Exception as e:
                pass
    for item in moveinfo.objects.all():
        smeargle=all_pokemon.objects.get(pokemon="Smeargle")
        ditto=all_pokemon.objects.get(pokemon="Ditto")
        id_=pokemon_moveset.objects.all().order_by('-id').first().id+1
        try:
            pokemon_moveset.objects.create(id=id_,pokemon=smeargle,moveinfo=item)
        except Exception as e:
            pass
        id_=pokemon_moveset.objects.all().order_by('-id').first().id+1
        try:
            pokemon_moveset.objects.create(id=id_,pokemon=ditto,moveinfo=item)
        except Exception as e:
            pass
    for item in all_pokemon.objects.all():
        data={}
        data[item.pokemon]={}
        data[item.pokemon]['basestats']={}
        data[item.pokemon]['basestats']['hp']=item.hp
        data[item.pokemon]['basestats']['attack']=item.attack
        data[item.pokemon]['basestats']['defense']=item.defense
        data[item.pokemon]['basestats']['s_attack']=item.s_attack
        data[item.pokemon]['basestats']['s_defense']=item.s_defense
        data[item.pokemon]['basestats']['speed']=item.speed
        data[item.pokemon]['basestats']['bst']=item.bst
        data[item.pokemon]['types']=[]
        for t in item.types.all():
            data[item.pokemon]['types'].append(t.typing)
        data[item.pokemon]['abilities']=[]
        for a in item.abilities.all():
            data[item.pokemon]['abilities'].append(a.ability)
        data[item.pokemon]['learnset']={}
        for move in item.moves.all():
            data[item.pokemon]['learnset'][move.moveinfo.name]={}
            data[item.pokemon]['learnset'][move.moveinfo.name]['Type']=move.moveinfo.move_typing
            data[item.pokemon]['learnset'][move.moveinfo.name]['Category']=move.moveinfo.move_category
            data[item.pokemon]['learnset'][move.moveinfo.name]['Power']=move.moveinfo.move_power
            data[item.pokemon]['learnset'][move.moveinfo.name]['Accuracy']=move.moveinfo.move_accuracy
            data[item.pokemon]['learnset'][move.moveinfo.name]['Priority']=move.moveinfo.move_priority
            data[item.pokemon]['learnset'][move.moveinfo.name]['Secondary Effect']=move.moveinfo.secondary_effect
            data[item.pokemon]['learnset'][move.moveinfo.name]['Secondary Effect Chance']=move.moveinfo.secondary_effect_chance
        data[item.pokemon]['typematchup']={}
        effectiveness=item.effectiveness
        data[item.pokemon]['typematchup']['Bug']=effectiveness.bug
        data[item.pokemon]['typematchup']['Dark']=effectiveness.dark
        data[item.pokemon]['typematchup']['Dragon']=effectiveness.dragon
        data[item.pokemon]['typematchup']['Electric']=effectiveness.electric
        data[item.pokemon]['typematchup']['Fairy']=effectiveness.fairy
        data[item.pokemon]['typematchup']['Fighting']=effectiveness.fighting
        data[item.pokemon]['typematchup']['Fire']=effectiveness.fire
        data[item.pokemon]['typematchup']['Flying']=effectiveness.flying
        data[item.pokemon]['typematchup']['Ghost']=effectiveness.ghost
        data[item.pokemon]['typematchup']['Grass']=effectiveness.grass
        data[item.pokemon]['typematchup']['Ground']=effectiveness.ground
        data[item.pokemon]['typematchup']['Ice']=effectiveness.ice
        data[item.pokemon]['typematchup']['Normal']=effectiveness.normal
        data[item.pokemon]['typematchup']['Poison']=effectiveness.poison
        data[item.pokemon]['typematchup']['Psychic']=effectiveness.psychic
        data[item.pokemon]['typematchup']['Rock']=effectiveness.rock
        data[item.pokemon]['typematchup']['Steel']=effectiveness.steel
        data[item.pokemon]['typematchup']['Water']=effectiveness.water
        data[item.pokemon]['sprites']={}
        sprites=item.sprite
        data[item.pokemon]['sprites']["swsh/ani/standard/PKMN.gif"]=sprites.dexani.url
        data[item.pokemon]['sprites']["swsh/ani/shiny/PKMN.gif"]=sprites.dexanishiny.url
        data[item.pokemon]['sprites']["swsh/png/standard/PKMN.png"]=sprites.dex.url
        data[item.pokemon]['sprites']["swsh/png/shiny/PKMN.png"]=sprites.dexshiny.url
        data[item.pokemon]['sprites']["bw/png/standard/PKMN.png"]=sprites.bw.url
        data[item.pokemon]['sprites']["bw/png/shiny/PKMN.png"]=sprites.bwshiny.url
        data[item.pokemon]['sprites']["afd/png/standard/PKMN.png"]=sprites.afd.url
        data[item.pokemon]['sprites']["afd/png/shiny/PKMN.png"]=sprites.afdshiny.url
        data=json.dumps(data)
        print(item.pokemon)
        item.data=data
        item.save()