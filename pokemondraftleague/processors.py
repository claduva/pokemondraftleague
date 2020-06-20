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
from pokemonadmin.models import *

def processor(request):
    try:
        leagueshosted = league.objects.all().filter(host=request.user).order_by('name')
    except Exception as e:
        leagueshosted = None
    allleagues = league.objects.all().exclude(name__icontains='Test').order_by('name')
    try:  
        leaguescoaching = coachdata.objects.all().filter(Q(coach=request.user)|Q(teammate=request.user)).order_by('league_name')
    except:
        leaguescoaching = None
    try:  
        userhistoricteams = historical_team.objects.all().filter(Q(coach1=request.user)|Q(coach2=request.user)).order_by('league__name','seasonname')
    except:
        userhistoricteams = None
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
        unreadmessages=messagelist.exclude(read=True).count()
    else:
        messagelist=None
        numberofmessages=0
        unreadmessages=0
    allpokemonlist=all_pokemon.objects.all().order_by('pokemon')
    return {
        'leagueshosted': leagueshosted,
        'allleagues': allleagues,
        'leaguescoaching': leaguescoaching,
        'userhistoricteams':userhistoricteams,
        'coachawards': coachawards,
        'site_settings': site_settings,
        'messagelist':messagelist,
        'numberofmessages': numberofmessages,
        'unreadmessages':unreadmessages,
        'allpokemonlist':allpokemonlist,
        }