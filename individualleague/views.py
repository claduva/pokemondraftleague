from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

import math

from .models import *
from leagues.models import *
from pokemondatabase.models import *
from .forms import *
import datetime as datetime

def team_page(request,league_name,team_abbreviation):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        team=coachdata.objects.filter(league_name=league_,teamabbreviation=team_abbreviation).first()
        try:
            season=seasonsetting.objects.get(league=league_)
            teamroster=roster.objects.all().filter(season=season,team=team).order_by('id')
        except:
            teamroster=None
        
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
        'roster': teamroster,
    }
    return render(request, 'teampage.html',context)

def league_draft(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
        print(request.user==league_.host)
        league_teams=coachdata.objects.all().filter(league_name=league_).order_by('teamname')
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        season=seasonsetting.objects.get(league=league_)
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    try:
        draftlist=draft.objects.all().filter(season=season).order_by('id') 
        draftsize=draftlist.count()
        picksremaining=draftlist.filter(pokemon__isnull=True).count()
        draftprogress=int(math.floor((draftsize-picksremaining)/draftsize*100))
    except:
        messages.error(request,'Draft does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    currentpick=draftlist.filter(pokemon__isnull=True).first()
    if currentpick==None:
        draftactive=False
        availablepoints=0
    else:
        draftactive=True
        draftersroster=roster.objects.all().filter(season=season,team=currentpick.team)
        pointsused=0
        for item in draftersroster:
            tier=pokemon_tier.objects.filter(league=league_,pokemon=item.pokemon).first()
            if tier != None:    
                pointsused+=tier.tier.tierpoints
        budget=season.draftbudget
        availablepoints=budget-pointsused
    if request.method == "POST":
        try:
            draftpick=all_pokemon.objects.get(pokemon=request.POST['draftpick'])
        except:
            messages.error(request,f'{request.POST["draftpick"]} is not a pokemon!',extra_tags='danger')
            return redirect('league_draft',league_name=league_name)
        searchroster=roster.objects.filter(season=season,pokemon=draftpick).first()
        if searchroster!=None:
            messages.error(request,f'{draftpick.pokemon } has already been drafted!',extra_tags='danger')
            return redirect('league_draft',league_name=league_name)
        currentpick.pokemon=draftpick
        rosterspot=roster.objects.all().order_by('id').filter(season=season,team=currentpick.team,pokemon__isnull=True).first()
        rosterspot.pokemon=draftpick
        currentpick.save()
        rosterspot.save()
        messages.success(request,'Your draft pick has been saved!')
        return redirect('league_draft',league_name=league_name)
    availablepokemon=all_pokemon.objects.all().order_by('pokemon')
    for item in availablepokemon:
        tiering=pokemon_tier.objects.all().filter(league=league_,pokemon=item).first()
        if tiering.tier.tiername=="Banned":
            availablepokemon=availablepokemon.all().exclude(pokemon=item)
        else:
            rosteritem=roster.objects.filter(season=season,pokemon=item).first()
            if rosteritem != None:
                availablepokemon=availablepokemon.all().exclude(pokemon=item)
    context = {
        'league': league_,
        'leaguepage': True,
        'league_name': league_name,
        'league_teams': league_teams,
        'draftlist': draftlist,
        'draftstartid': -(draftlist.first().id-1),
        'currentpick':currentpick,
        'availablepokemon': availablepokemon,
        'draftactive': draftactive,
        'availablepoints':availablepoints,
        'draftprogress':draftprogress,
    }
    return render(request, 'draft.html',context)

@login_required
def create_match(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user != league_.host:
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    leaguesettings=league_settings.objects.get(league_name=league_)
    needednumberofcoaches=leaguesettings.number_of_teams
    currentcoaches=coachdata.objects.filter(league_name=league_)
    currentcoachescount=len(currentcoaches)
    try:
        seasonsettings=seasonsetting.objects.get(league=league_)
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if needednumberofcoaches != currentcoachescount: 
        messages.error(request,'You can only utilize season settings if you have designated the same number of coaches as available spots',extra_tags='danger')
        return redirect('individual_league_settings',league_name=league_name)
    if request.method == 'POST':   
        form = CreateMatchForm(seasonsettings,league_,request.POST)
        if form.is_valid() :
            form.save()
            messages.success(request,'That match has been added!')
        return redirect('create_match',league_name=league_name)
    form = CreateMatchForm(seasonsettings,league_,initial={'season':seasonsettings})
    settingheading='Create New Match'
    create=True
    manageseason=False
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'forms': [form],
        'seasonsettings': seasonsettings,
        'settingheading': settingheading,
        'create': create,
        'manageseason': manageseason,
    }
    return render(request, 'settings.html',context)

def league_schedule(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        season=seasonsetting.objects.get(league=league_)
    except:
        messages.error(request,'Season does not exist!',extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    leagueschedule=[]
    numberofweeks=season.seasonlength
    for i in range(numberofweeks):
        matches=schedule.objects.all().filter(week=str(i+1))
        leagueschedule.append(matches)
    context = {
        'league': league_,
        'leaguepage': True,
        'league_name': league_name,
        'leagueschedule': leagueschedule,
    }
    return render(request, 'schedule.html',context)