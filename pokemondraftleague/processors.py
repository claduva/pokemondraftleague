from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from leagues.models import *
from accounts.models import *
from pokemondatabase.models import *

def processor(request):
    try:
        leagueshosted = request.user.league_set.all().order_by('name')
    except:
        leagueshosted = None
    try:  
        allleagues = league.objects.all().order_by('name')
    except:
        allleagues = None
    try:  
        leaguescoaching = request.user.coachdata_set.all().order_by('league_name')
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
    
    return {
        'leagueshosted': leagueshosted,
        'allleagues': allleagues,
        'leaguescoaching': leaguescoaching,
        'coachawards': coachawards,
        'site_settings': site_settings,
        }