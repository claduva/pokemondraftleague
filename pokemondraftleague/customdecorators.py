from django.shortcuts import render, redirect
from django.contrib import messages
from leagues.models import *
from individualleague.models import *
from pokemonadmin.models import *

def check_if_league(view):
    def wrap(request, *args, **kwargs):
        try:
            league_=league.objects.get(name=kwargs['league_name'].replace("_"," "))
            return view(request, *args, **kwargs)
        except Exception as e:
            #raise(e)
            messages.error(request,'League does not exist!',extra_tags='danger')
            error_message.objects.create(
                associated_view=str(request),
                error_message=str(e)
            )
            return redirect('league_list')
    return wrap

def check_if_subleague(view):
    def wrap(request, *args, **kwargs):
        try:
            league_=league_subleague.objects.filter(league__name=kwargs['league_name'].replace("_"," ")).get(subleague=kwargs['subleague_name'].replace("_"," "))
            return view(request, *args, **kwargs)
        except Exception as e:
            #raise(e)
            print('subleague')
            messages.error(request,'League does not exist!',extra_tags='danger')
            error_message.objects.create(
                associated_view=str(request),
                error_message=str(e)
            )
            return redirect('league_list')
    return wrap

def check_if_season(view):
    def wrap(request, *args, **kwargs):
        try:
            season=seasonsetting.objects.filter(subleague__league__name=kwargs['league_name'].replace("_"," ")).get(subleague__subleague=kwargs['subleague_name'].replace("_"," "))
            return view(request, *args, **kwargs)
        except Exception as e:
            print(e)
            messages.error(request,'Season does not exist!',extra_tags='danger')
            error_message.objects.create(
                associated_view=str(request),
                error_message=str(e)
            )
            return redirect('league_detail',league_name=kwargs['league_name'])
    return wrap

def check_if_team(view):
    def wrap(request, *args, **kwargs):
        try:
            team=coachdata.objects.filter(league_name__name=kwargs['league_name'].replace("_"," "),subleague__subleague=kwargs['subleague_name'].replace("_"," ")).get(teamabbreviation=kwargs['team_abbreviation'])
            return view(request, *args, **kwargs)
        except Exception as e:
            print('team')
            messages.error(request,'Team does not exist!',extra_tags='danger')
            error_message.objects.create(
                associated_view=str(request),
                error_message=str(e)
            )
            return redirect('league_detail',league_name=kwargs['league_name']) 
    return wrap

def check_if_host(view):
    def wrap(request, *args, **kwargs):
        league_=league.objects.get(name=kwargs['league_name'])
        if request.user not in league_.host.all():
            messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
            return redirect('leagues_hosted_settings')
        else:    
            return view(request, *args, **kwargs)
    return wrap

def check_if_clad(view):
    def wrap(request, *args, **kwargs):
        if request.user.username!="claduva":
            return redirect('home')
        else:    
            return view(request, *args, **kwargs)
    return wrap

def check_if_match(view):
    def wrap(request, *args, **kwargs):
        try:
            match=schedule.objects.get(pk=kwargs['matchid'])
            print(match)
            return view(request, *args, **kwargs)
        except Exception as e:
            #raise(e)
            print('match')
            messages.error(request,'Match does not exist!',extra_tags='danger')
            error_message.objects.create(
                associated_view=str(request),
                error_message=str(e)
            )
            return redirect('league_schedule',league_name=kwargs['league_name'],subleague_name=kwargs['subleague_name'])
    return wrap