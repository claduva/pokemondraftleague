from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import *
from pokemondatabase.models import *

def team_page(request,league_name,team_abbreviation):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        team=coachdata.objects.filter(league_name=league_,teamabbreviation=team_abbreviation).first()
    except:
        messages.error(request,'Team does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name) 
    league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
    context = {
        'league': league_,
        'leaguepage': True,
        'league_name': league_name,
        'league_teams': league_teams,
        'team': team,
    }
    return render(request, 'teampage.html',context)

