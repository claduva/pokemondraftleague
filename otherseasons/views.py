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

from replayanalysis.helperfunctions import *
from replayanalysis.NewParser.parser import *
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
    season_teams=historical_team.objects.all().filter(league__name=league_name,seasonname=seasonofinterest).order_by('subseason')
    season=season_teams.first()
    if season==None:
        messages.error(request,'Season does not exist',extra_tags='danger')
        return redirect('home')
    otherseasons=historical_team.objects.all().filter(league__name=league_name).distinct('seasonname')
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
    roster=teamofinterest_.historical_roster.all().exclude(pokemon__isnull=True)
    draft=teamofinterest_.historical_draft.all().exclude(pokemon__isnull=True)
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
    draftlist=historical_draft.objects.all().filter(team__seasonname=seasonofinterest,team__league=league_)
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
        'draftlist':draftlist,
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
    free_agencies=historical_freeagency.objects.all().filter(team__league=league_,team__seasonname=season.seasonname).order_by('team__teamname')
    trades_=historical_trading.objects.all().filter(team__league=league_,team__seasonname=season.seasonname).order_by('id')
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
    otherseasons=historical_team.objects.all().filter(league__name=league_name).distinct('seasonname').exclude(seasonname=seasonofinterest)
    seasonschedule=historical_match.objects.all().filter(team1__league=league_,team1__seasonname=season.seasonname).exclude(week__contains="Playoff").order_by('week')
    context = {
        'league': league_,
        'otherseason':True,
        'season':season,
        'league_name':league_name,
        'otherseasons':otherseasons,
        'season_teams':season_teams,
        'seasonschedule':seasonschedule,
        'season_teams':season_teams,
    }
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
    otherseasons=historical_team.objects.all().filter(league__name=league_name).distinct('seasonname').exclude(seasonname=seasonofinterest)
    seasonschedule=historical_match.objects.all().filter(team1__league=league_,team1__seasonname=season.seasonname).filter(week__contains="Playoff").order_by('week')
    context = {
        'league': league_,
        'otherseason':True,
        'season':season,
        'league_name':league_name,
        'otherseasons':otherseasons,
        'season_teams':season_teams,
        'seasonschedule':seasonschedule,
        'season_teams':season_teams,
        'playoffs':True,
    }
    return render(request, 'otherseasonschedule.html',context)

def seasonreplay(request,league_name,seasonofinterest,matchid):
    clad=User.objects.get(username="claduva")
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
    try:
        results = match.match_replay.data
    except:
        url=match.replay
        try:    
            results = newreplayparse(url)
        except Exception as e:
            inbox.objects.create(sender=request.user,recipient=clad, messagesubject="Replay Error",messagebody=url)
            messages.error(request,f'There was an error processing your replay. claduva has been notified.',extra_tags="danger")
            raise(e)
        if len(results['errormessage'])!=0:
            inbox.objects.create(sender=request.user,recipient=clad, messagesubject="Replay Error",messagebody=url) 
    context={
        'results': results,
        'matchid':matchid,
        'league': league_,
        'league_name': league_.name,
        'otherseason':True,
        'season':season,
        'otherseasons':otherseasons,
        'season_teams':season_teams,
    }
    return render(request,"replayanalysisresults.html",context)

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