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

def otherseasonslist(request,league_name):
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