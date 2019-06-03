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

from leagues.models import *
from accounts.models import *
from pokemondatabase.models import *



def processor(request):
    try:
        leagueshosted = request.user.league_set.all().order_by('name')
    except:
        leagueshosted = None
    try:  
        allleagues = league.objects.all().filter().order_by('name')
        for item in allleagues:
            settings=league_settings.objects.get(league_name=item)
            if settings.is_public==False and item.host != request.user:
                allleagues=allleagues.exclude(pk=item.id)
        
    except:
        allleagues = None
    try:  
        leaguescoaching = coachdata.objects.all().filter(Q(coach=request.user)|Q(teammate=request.user)).order_by('league_name')
    except:
        leaguescoaching = None
    try:  
        coachawards = request.user.coachaward_set.all()
    except:
        coachawards = None
    try:  
        site_settings = request.user.sitesettings
    except:
        user=User.objects.get(username="defaultuser")
        site_settings = user.sitesettings
    if request.user.is_authenticated:
        messagelist=inbox.objects.all().filter(recipient=request.user)
        numberofmessages=messagelist.count()
    else:
        messagelist=None
        numberofmessages=0
    allpokemonlist=all_pokemon.objects.all()
    
    unexecutedfa=free_agency.objects.all().filter(executed=False)
    #process unexecuted free agencies
    for item in unexecutedfa:
        #get league start date
        timezone = pytz.timezone('UTC')
        request_league=seasonsetting.objects.get(league=item.season.league)
        league_start=request_league.seasonstart
        elapsed=item.timeadded-league_start
        requestedweek=math.ceil(elapsed.total_seconds()/60/60/24/7)
        elapsed=timezone.localize(datetime.now())-league_start
        currentweek=math.ceil(elapsed.total_seconds()/60/60/24/7)
        completedmatches=True
        for i in range(1,requestedweek+1):
            matchofinterest=schedule.objects.filter(season=item.season).filter(Q(team1=item.coach)|Q(team2=item.coach)).get(week=str(i))
            if matchofinterest.replay=="Link":
                completedmatches=False
        print(completedmatches)
        
    return {
        'leagueshosted': leagueshosted,
        'allleagues': allleagues,
        'leaguescoaching': leaguescoaching,
        'coachawards': coachawards,
        'site_settings': site_settings,
        'messagelist':messagelist,
        'numberofmessages': numberofmessages,
        'allpokemonlist':allpokemonlist,
        }