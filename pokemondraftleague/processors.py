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

def processor(request):
    try:
        leagueshosted = request.user.league_set.all().order_by('name')
    except:
        leagueshosted = None
    try:  
        allleagues = league.objects.all().order_by('name')
    except:
        allleagues = None
    return {
        'leagueshosted': leagueshosted,
        'allleagues': allleagues,
        }