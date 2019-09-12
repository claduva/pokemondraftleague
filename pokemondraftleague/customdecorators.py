
from django.shortcuts import render, redirect
from django.contrib import messages
from leagues.models import *

def check_if_league(view):
    def wrap(request, *args, **kwargs):
        try:
            league_=league.objects.get(name=kwargs['league_name'])
            return view(request, *args, **kwargs)
        except Exception as e:
            print(e)
            messages.error(request,'League does not exist!',extra_tags='danger')
            return redirect('league_list')
    return wrap


def check_if_subleague(view):
    def wrap(request, *args, **kwargs):
        try:
            league_=league_subleague.objects.filter(league__name=kwargs['league_name'])
            print(league_)
            league_=league_.get(subleague=kwargs['subleague_name'])
            return view(request, *args, **kwargs)
        except Exception as e:
            print(e)
            messages.error(request,'League does not exist!',extra_tags='danger')
            return redirect('league_list')
    return wrap

def check_if_season(view):
    def wrap(request, *args, **kwargs):
        try:
            season=seasonsetting.objects.get(league__name=kwargs['league_name'])  
            return view(request, *args, **kwargs)
        except Exception as e:
            print(e)
            messages.error(request,'Season does not exist!',extra_tags='danger')
            return redirect('league_detail',league_name=kwargs['league_name'])
    return wrap

def check_if_team(view):
    def wrap(request, *args, **kwargs):
        try:
            team=coachdata.objects.filter(league_name__name=kwargs['league_name']).get(teamabbreviation=kwargs['team_abbreviation'])
            return view(request, *args, **kwargs)
        except Exception as e:
            print(e)
            messages.error(request,'Team does not exist!',extra_tags='danger')
            return redirect('league_detail',league_name=kwargs['league_name']) 
    return wrap