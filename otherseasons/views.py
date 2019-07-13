from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q

from datetime import datetime, timezone, timedelta
import pytz
import math

from .forms import *
from .models import *
from leagues.models import league_team
from pokemondatabase.models import *
from pokemonadmin.models import *
from individualleague.models import *
from accounts.models import *

from replayanalysis.ShowdownReplayParser.replayparser import *
from replayanalysis.helperfunctions import *

def otherseasonslist(request,league_name):
    league_name=league_name.replace('_',' ')
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist',extra_tags='danger')
        return redirect('home')
    otherseasons=historical_team.objects.all().filter(league__name=league_name).distinct('seasonname')
    context = {
        'league': league_,
        'otherseasons':otherseasons,
        'league_name':league_name,
    }
    return render(request, 'otherseasons.html',context)

def seasondetail(request,league_name,seasonofinterest):
    seasonofinterest=seasonofinterest.replace('_',' ')
    league_name=league_name.replace('_',' ')
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist',extra_tags='danger')
        return redirect('home')
    season_teams=historical_team.objects.all().filter(league__name=league_name,seasonname=seasonofinterest)    
    season=season_teams.first()
    if season==None:
        messages.error(request,'Season does not exist',extra_tags='danger')
        return redirect('home')
    otherseasons=historical_team.objects.all().filter(league__name=league_name).distinct('seasonname').exclude(seasonname=seasonofinterest)
    context = {
        'league': league_,
        'otherseason':True,
        'season':season,
        'league_name':league_name,
        'otherseasons':otherseasons,
        'season_teams':season_teams,
    }
    return render(request, 'otherseasons.html',context)

def seasonteamdetail(request,league_name,seasonofinterest,teamofinterest):
    seasonofinterest=seasonofinterest.replace('_',' ')
    teamofinterest=teamofinterest.replace('_',' ')
    league_name=league_name.replace('_',' ')
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist',extra_tags='danger')
        return redirect('home')
    season_teams=historical_team.objects.all().filter(league__name=league_name,seasonname=seasonofinterest)    
    season=season_teams.first()
    if season==None:
        messages.error(request,'Season does not exist',extra_tags='danger')
        return redirect('home')
    try:
        teamofinterest_=season_teams.get(teamname=teamofinterest)
    except:
        messages.error(request,'Team does not exist',extra_tags='danger')
        return redirect('home')
    otherseasons=historical_team.objects.all().filter(league__name=league_name).distinct('seasonname').exclude(seasonname=seasonofinterest)
    roster=teamofinterest_.historical_roster.all()
    draft=teamofinterest_.historical_draft.all()
    context = {
        'league': league_,
        'otherseason':True,
        'season':season,
        'league_name':league_name,
        'otherseasons':otherseasons,
        'season_teams':season_teams,
        'teamofinterest':teamofinterest_,
        'roster':roster,
        'draft':draft
    }
    return render(request, 'otherseasons_team_detail.html',context)

def seasondraft(request,league_name,seasonofinterest):
    seasonofinterest=seasonofinterest.replace('_',' ')
    league_name=league_name.replace('_',' ')
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist',extra_tags='danger')
        return redirect('home')
    season_teams=historical_team.objects.all().filter(league__name=league_name,seasonname=seasonofinterest)    
    season=season_teams.first()
    if season==None:
        messages.error(request,'Season does not exist',extra_tags='danger')
        return redirect('home')
    otherseasons=historical_team.objects.all().filter(league__name=league_name).distinct('seasonname').exclude(seasonname=seasonofinterest)
    context = {
        'league': league_,
        'otherseason':True,
        'season':season,
        'league_name':league_name,
        'otherseasons':otherseasons,
        'season_teams':season_teams,
    }
    return render(request, 'otherseasondraft.html',context)

def seasontransactions(request,league_name,seasonofinterest):
    seasonofinterest=seasonofinterest.replace('_',' ')
    league_name=league_name.replace('_',' ')
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist',extra_tags='danger')
        return redirect('home')
    season_teams=historical_team.objects.all().filter(league__name=league_name,seasonname=seasonofinterest)    
    season=season_teams.first()
    if season==None:
        messages.error(request,'Season does not exist',extra_tags='danger')
        return redirect('home')
    otherseasons=historical_team.objects.all().filter(league__name=league_name).distinct('seasonname').exclude(seasonname=seasonofinterest)
    free_agencies=historical_freeagency.objects.all().filter(team__seasonname=season.seasonname).order_by('team__teamname')
    trades_=historical_trading.objects.all().filter(team__seasonname=season.seasonname)
    trades=[]
    i=0
    for item in trades_:
        if i%2==0:
            trade=[item]
        else:
            trade.append(item.team)
            trades.append(trade)
        i+=1
    context = {
        'league': league_,
        'otherseason':True,
        'season':season,
        'league_name':league_name,
        'otherseasons':otherseasons,
        'season_teams':season_teams,
        'free_agencies': free_agencies,
        'trades': trades,
    }
    return render(request, 'otherseasontransactions.html',context)

def seasonschedule(request,league_name,seasonofinterest):
    seasonofinterest=seasonofinterest.replace('_',' ')
    league_name=league_name.replace('_',' ')
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist',extra_tags='danger')
        return redirect('home')
    season_teams=historical_team.objects.all().filter(league__name=league_name,seasonname=seasonofinterest)    
    season=season_teams.first()
    if season==None:
        messages.error(request,'Season does not exist',extra_tags='danger')
        return redirect('home')
    leagueschedule=[]
    numberofweeks=historical_match.objects.all().distinct('week').exclude(week__contains="Playoffs").count()
    for i in range(numberofweeks):
        matches=historical_match.objects.all().filter(week=str(i+1),team1__league=league_,team1__seasonname=season.seasonname).order_by('id')
        leagueschedule.append([str(i+1),matches])
    otherseasons=historical_team.objects.all().filter(league__name=league_name).distinct('seasonname').exclude(seasonname=seasonofinterest)
    context = {
        'league': league_,
        'otherseason':True,
        'season':season,
        'league_name':league_name,
        'otherseasons':otherseasons,
        'season_teams':season_teams,
        'leagueschedule': leagueschedule,
        'numberofweeks': range(numberofweeks),
    }
    if request.method=="POST":
        if request.POST['purpose']=="Go":
            weekselect=request.POST['weekselect']
            if weekselect=="All":
                donothing=True
            else:
                matches=historical_match.objects.all().filter(week=weekselect,team1__league=league_,team1__seasonname=season.seasonname).order_by('id')
                leagueschedule=[[weekselect,matches]]
                context.update({'leagueschedule':leagueschedule})
    return render(request, 'otherseasonschedule.html',context)

def seasonplayoffs(request,league_name,seasonofinterest):
    seasonofinterest=seasonofinterest.replace('_',' ')
    league_name=league_name.replace('_',' ')
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist',extra_tags='danger')
        return redirect('home')
    season_teams=historical_team.objects.all().filter(league__name=league_name,seasonname=seasonofinterest)
    season=season_teams.first()
    if season==None:
        messages.error(request,'Season does not exist',extra_tags='danger')
        return redirect('home')
    leagueschedule=[]
    playoffweeks=historical_match.objects.all().filter(week__contains="Playoffs").order_by('id')
    priorweeks=[]
    for item in playoffweeks:
        matches=historical_match.objects.all().filter(week=item.week,team1__league=league_,team1__seasonname=season.seasonname).order_by('id')
        if item.week not in priorweeks:    
            leagueschedule.append([item.week,matches])
            priorweeks.append(item.week)
       
    otherseasons=historical_team.objects.all().filter(league__name=league_name).distinct('seasonname').exclude(seasonname=seasonofinterest)
    context = {
        'league': league_,
        'otherseason':True,
        'season':season,
        'league_name':league_name,
        'otherseasons':otherseasons,
        'season_teams':season_teams,
        'leagueschedule': leagueschedule,
        'numberofweeks': range(playoffweeks.count()),
        'playoffs':True,
    }
    if request.method=="POST":
        if request.POST['purpose']=="Go":
            weekselect=request.POST['weekselect']
            if weekselect=="All":
                donothing=True
            else:
                matches=historical_match.objects.all().filter(week=weekselect,team1__league=league_,team1__seasonname=season.seasonname).order_by('id')
                leagueschedule=[[weekselect,matches]]
                context.update({'leagueschedule':leagueschedule})
    return render(request, 'otherseasonschedule.html',context)

def seasonreplay(request,league_name,seasonofinterest,matchid):
    seasonofinterest=seasonofinterest.replace('_',' ')
    league_name=league_name.replace('_',' ')
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist',extra_tags='danger')
        return redirect('home')
    season_teams=historical_team.objects.all().filter(league__name=league_name,seasonname=seasonofinterest)
    season=season_teams.first()
    if season==None:
        messages.error(request,'Season does not exist',extra_tags='danger')
        return redirect('home')
    try:
        match=historical_match.objects.get(pk=matchid)
        if match.replay == "":
            messages.error(request,f'A replay for that match does not exist!',extra_tags="danger")
            return redirect('seasonschedule',league_name=league_name,seasonofinterest=seasonofinterest)
    except:
        return redirect('seasonschedule',league_name=league_name,seasonofinterest=seasonofinterest)
    otherseasons=historical_team.objects.all().filter(league__name=league_name).distinct('seasonname')
    url=match.replay
    outputstring, team1, team2 = replayparse(url)
    coach1=team1.coach
    coach2=team2.coach 
    coach1alt=showdownalts.objects.all().filter(showdownalt=coach1).first()
    coach2alt=showdownalts.objects.all().filter(showdownalt=coach2).first()
    coach1team=coachdata.objects.all().filter(league_name=league_).filter(Q(coach=coach1alt.user)|Q(teammate=coach1alt.user)).first()
    coach2team=coachdata.objects.all().filter(league_name=league_).filter(Q(coach=coach2alt.user)|Q(teammate=coach2alt.user)).first()
    context={
        'output': outputstring,
        'team1':team1,
        'team2':team2,
        'team1name':coach1team,
        'team2name':coach2team,
        'replay': url,
        'league_name':league_name,
        'matchid':matchid,
        'showreplay': True,
        'league': league_,
        'otherseason':True,
        'season':season,
        'otherseasons':otherseasons,
        'season_teams':season_teams,
    }
    return render(request,"replayanalysisform.html",context)

def seasonleagueleaders(request,league_name,seasonofinterest):
    seasonofinterest=seasonofinterest.replace('_',' ')
    league_name=league_name.replace('_',' ')
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist',extra_tags='danger')
        return redirect('home')
    season_teams=historical_team.objects.all().filter(league__name=league_name,seasonname=seasonofinterest)
    season=season_teams.first()
    if season==None:
        messages.error(request,'Season does not exist',extra_tags='danger')
        return redirect('home')
    otherseasons=historical_team.objects.all().filter(league__name=league_name).distinct('seasonname')
    leagueleaders=historical_roster.objects.all().filter(team__seasonname=season.seasonname,gp__gt=0).order_by('-kills','-differential')
    context = {
        'league': league_,
        'league_name': league_name,
        'otherseason':True,
        'season':season,
        'otherseasons':otherseasons,
        'season_teams':season_teams,
        'leagueleaders': leagueleaders,
    }
    return render(request, 'leagueleaders.html',context)

def seasonhalloffame(request,league_name,seasonofinterest):
    seasonofinterest=seasonofinterest.replace('_',' ')
    league_name=league_name.replace('_',' ')
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist',extra_tags='danger')
        return redirect('home')
    season_teams=historical_team.objects.all().filter(league__name=league_name,seasonname=seasonofinterest)
    season=season_teams.first()
    if season==None:
        messages.error(request,'Season does not exist',extra_tags='danger')
        return redirect('home')
    otherseasons=historical_team.objects.all().filter(league__name=league_name).distinct('seasonname')
    championship=historical_match.objects.all().filter(team1__seasonname=season.seasonname,team1__league=league_).get(week="Playoffs Finals")
    champion=championship.winner
    if championship.team1==champion:
        runnerup=championship.team2
    else:
        runnerup=championship.team1
    
    context = {
        'league': league_,
        'league_name': league_name,
        'otherseason':True,
        'season':season,
        'otherseasons':otherseasons,
        'season_teams':season_teams,
        'champion':champion,
        'runnerup':runnerup,
    }
    return render(request, 'otherseasonhof.html',context)