from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import json
from datetime import datetime
import time

from .models import *
from .forms import *
from leagues.models import *
from accounts.models import showdownalts
from .ShowdownReplayParser.replayparser import *

# Create your views here.
def replay_analysis(request):
    if request.method=="POST":
        form = MatchReplayForm(request.POST)
        if form.is_valid():
            url=form.cleaned_data['url']
            outputstring, team1, team2 = replayparse(url)
            context={
                'output': outputstring,
                'team1':team1,
                'team2':team2,
                'replay': url,
            }
            return render(request,"replayanalysisform.html",context)
    form=MatchReplayForm()
    context={
        'form': form,
        'submission': True,
    }
    return  render(request,"replayanalysisform.html",context)

@login_required
def upload_league_replay(request,league_name,matchid):
    try:
        league_=league.objects.get(name=league_name)
    except:
        return redirect('league_list')
    try:
        match=schedule.objects.get(pk=matchid)
        if match.replay != "Link":
            messages.error(request,f'A replay for that match already exists!',extra_tags="danger")
            return redirect('league_schedule',league_name=league_name)
    except:
        return redirect('league_schedule',league_name=league_name)
    if request.method=="POST":
        form = LeagueReplayForm(request.POST,instance=match)
        if form.is_valid():
            url=form.cleaned_data['replay']
            outputstring, team1, team2 = replayparse(url)
            coach1=team1.coach
            coach2=team2.coach
            try:
                coach1alt=showdownalts.objects.get(showdownalt=coach1)
                coach2alt=showdownalts.objects.get(showdownalt=coach2)
                coach1team=coachdata.objects.all().filter(league_name=league_).get(coach=coach1alt.user)
                coach2team=coachdata.objects.all().filter(league_name=league_).get(coach=coach2alt.user)
            except:
                messages.error('A matching showdown alt for one or both coachs was not found!',extra_tags='danger')
                return redirect('schedule',league_name=league_name)
            context={
                'output': outputstring,
                'team1':team1,
                'team2':team2,
                'team1name':coach1team,
                'team2name':coach2team,
                'replay': url,
                'confirm': True,
                'form': form,
                'league_name':league_name,
                'matchid':matchid,
                'league': league_,
                'leaguepage': True,
            }
            return render(request,"replayanalysisform.html",context)
    form=LeagueReplayForm(instance=match,initial={"replay":""})
    context={
        'form': form,
        'submission': True,
        'league_name':league_name,
        'matchid':matchid,
        'league': league_,
        'leaguepage': True,
    }
    return  render(request,"replayanalysisform.html",context)

@login_required
def confirm_league_replay(request,league_name,matchid):
    try:
        league_=league.objects.get(name=league_name)
    except:
        return redirect('league_list')
    try:
        season=league_.seasonsetting
    except:
        return redirect('league_list')
    try:
        match=schedule.objects.get(pk=matchid)
    except:
        return redirect('league_schedule',league_name=league_name)
    if request.method=="POST":
        form = LeagueReplayForm(request.POST,instance=match)
        if form.is_valid():
            url=form.cleaned_data['replay']
            outputstring, team1, team2 = replayparse(url)
            coach1=team1.coach
            coach2=team2.coach
            try:
                coach1alt=showdownalts.objects.get(showdownalt=coach1)
                coach1team=coachdata.objects.all().filter(league_name=league_).get(coach=coach1alt.user)
            except:
                messages.error(request,f'No coach matching {team1.coach} could be found!',extra_tags="danger")
                return redirect('league_schedule',league_name=league_name)
            try:
                coach2alt=showdownalts.objects.get(showdownalt=coach2)
                coach2team=coachdata.objects.all().filter(league_name=league_).get(coach=coach2alt.user)
            except:
                messages.error(request,f'No coach matching {team1.coach} could be found!',extra_tags="danger")
                return redirect('league_schedule',league_name=league_name)
            #update team1 pokemon data
            try:
                pokemon=all_pokemon.objects.get(pokemon=team1.pokemon1)
                t1pokemon1=roster.objects.all().filter(season=season,team=coach1team).get(pokemon=pokemon)
            except:
                messages.error(request,f'A match for {team1.pokemon1} could not be found!',extra_tags="danger")
                return redirect('league_schedule',league_name=league_name)
            try:
                pokemon=all_pokemon.objects.get(pokemon=team1.pokemon2)
                t1pokemon2=roster.objects.all().filter(season=season,team=coach1team).get(pokemon=pokemon)
            except:
                messages.error(request,f'A match for {team1.pokemon2} could not be found!',extra_tags="danger")
                return redirect('league_schedule',league_name=league_name)
            try:    
                pokemon=all_pokemon.objects.get(pokemon=team1.pokemon3)
                t1pokemon3=roster.objects.all().filter(season=season,team=coach1team).get(pokemon=pokemon)
            except:
                messages.error(request,f'A match for {team1.pokemon3} could not be found!',extra_tags="danger")
                return redirect('league_schedule',league_name=league_name)
            try:    
                pokemon=all_pokemon.objects.get(pokemon=team1.pokemon4)
                t1pokemon4=roster.objects.all().filter(season=season,team=coach1team).get(pokemon=pokemon)
            except:
                messages.error(request,f'A match for {team1.pokemon4} could not be found!',extra_tags="danger")
                return redirect('league_schedule',league_name=league_name)
            try:    
                pokemon=all_pokemon.objects.get(pokemon=team1.pokemon5)
                t1pokemon5=roster.objects.all().filter(season=season,team=coach1team).get(pokemon=pokemon)
            except:
                messages.error(request,f'A match for {team1.pokemon5} could not be found!',extra_tags="danger")
                return redirect('league_schedule',league_name=league_name)
            try:    
                pokemon=all_pokemon.objects.get(pokemon=team1.pokemon6)
                t1pokemon6=roster.objects.all().filter(season=season,team=coach1team).get(pokemon=pokemon)
            except:
                messages.error(request,f'A match for {team1.pokemon6} could not be found!',extra_tags="danger")
                return redirect('league_schedule',league_name=league_name)
            t1pokemon1.kills+=team1.P1K
            t1pokemon1.deaths+=team1.P1F
            t1pokemon1.differential+=team1.P1Diff
            t1pokemon1.gp+=1
            t1pokemon1.gw+=team1.win
            t1pokemon2.kills+=team1.P2K
            t1pokemon2.deaths+=team1.P2F
            t1pokemon2.differential+=team1.P2Diff
            t1pokemon2.gp+=1
            t1pokemon2.gw+=team1.win
            t1pokemon3.kills+=team1.P3K
            t1pokemon3.deaths+=team1.P3F
            t1pokemon3.differential+=team1.P3Diff
            t1pokemon3.gp+=1
            t1pokemon3.gw+=team1.win
            t1pokemon4.kills+=team1.P4K
            t1pokemon4.deaths+=team1.P4F
            t1pokemon4.differential+=team1.P4Diff
            t1pokemon4.gp+=1
            t1pokemon4.gw+=team1.win
            t1pokemon5.kills+=team1.P5K
            t1pokemon5.deaths+=team1.P5F
            t1pokemon5.differential+=team1.P5Diff
            t1pokemon5.gp+=1
            t1pokemon5.gw+=team1.win
            t1pokemon6.kills+=team1.P6K
            t1pokemon6.deaths+=team1.P6F
            t1pokemon6.differential+=team1.P6Diff
            t1pokemon6.gp+=1
            t1pokemon6.gw+=team1.win
            #update team2 pokemon data
            try:
                pokemon=all_pokemon.objects.get(pokemon=team2.pokemon1)
                t2pokemon1=roster.objects.all().filter(season=season,team=coach2team).get(pokemon=pokemon)
            except:
                messages.error(request,f'A match for {team2.pokemon1} could not be found!',extra_tags="danger")
                return redirect('league_schedule',league_name=league_name)
            try:
                pokemon=all_pokemon.objects.get(pokemon=team2.pokemon2)
                t2pokemon2=roster.objects.all().filter(season=season,team=coach2team).get(pokemon=pokemon)
            except:
                messages.error(request,f'A match for {team2.pokemon2} could not be found!',extra_tags="danger")
                return redirect('league_schedule',league_name=league_name)
            try:    
                pokemon=all_pokemon.objects.get(pokemon=team2.pokemon3)
                t2pokemon3=roster.objects.all().filter(season=season,team=coach2team).get(pokemon=pokemon)
            except:
                messages.error(request,f'A match for {team2.pokemon3} could not be found!',extra_tags="danger")
                return redirect('league_schedule',league_name=league_name)
            try:    
                pokemon=all_pokemon.objects.get(pokemon=team2.pokemon4)
                t2pokemon4=roster.objects.all().filter(season=season,team=coach2team).get(pokemon=pokemon)
            except:
                messages.error(request,f'A match for {team2.pokemon4} could not be found!',extra_tags="danger")
                return redirect('league_schedule',league_name=league_name)
            try:    
                pokemon=all_pokemon.objects.get(pokemon=team2.pokemon5)
                t2pokemon5=roster.objects.all().filter(season=season,team=coach2team).get(pokemon=pokemon)
            except:
                messages.error(request,f'A match for {team2.pokemon5} could not be found!',extra_tags="danger")
                return redirect('league_schedule',league_name=league_name)
            try:    
                pokemon=all_pokemon.objects.get(pokemon=team2.pokemon6)
                t2pokemon6=roster.objects.all().filter(season=season,team=coach2team).get(pokemon=pokemon)
            except:
                messages.error(request,f'A match for {team2.pokemon6} could not be found!',extra_tags="danger")
                return redirect('league_schedule',league_name=league_name)
            t2pokemon1.kills+=team2.P1K
            t2pokemon1.deaths+=team2.P1F
            t2pokemon1.differential+=team2.P1Diff
            t2pokemon1.gp+=1
            t2pokemon1.gw+=team2.win
            t2pokemon2.kills+=team2.P2K
            t2pokemon2.deaths+=team2.P2F
            t2pokemon2.differential+=team2.P2Diff
            t2pokemon2.gp+=1
            t2pokemon2.gw+=team2.win
            t2pokemon3.kills+=team2.P3K
            t2pokemon3.deaths+=team2.P3F
            t2pokemon3.differential+=team2.P3Diff
            t2pokemon3.gp+=1
            t2pokemon3.gw+=team2.win
            t2pokemon4.kills+=team2.P4K
            t2pokemon4.deaths+=team2.P4F
            t2pokemon4.differential+=team2.P4Diff
            t2pokemon4.gp+=1
            t2pokemon4.gw+=team2.win
            t2pokemon5.kills+=team2.P5K
            t2pokemon5.deaths+=team2.P5F
            t2pokemon5.differential+=team2.P5Diff
            t2pokemon5.gp+=1
            t2pokemon5.gw+=team2.win
            t2pokemon6.kills+=team2.P6K
            t2pokemon6.deaths+=team2.P6F
            t2pokemon6.differential+=team2.P6Diff
            t2pokemon6.gp+=1
            t2pokemon6.gw+=team2.win
            #update coach1 data
            coach1team.wins+=team1.win
            coach1team.losses+=abs(team1.win-1)
            coach1team.forfeit+=team1.forfeit
            if team1.forfeit == 1:
                coach1team.differential+=(-6)
            else:
                coach1team.differential+=team1.diff
            if coach1team.streak < 0:
                if team1.win == 1:
                    coach1team.streak=1
                else:
                    coach1team.streak+=(-1)
            else:
                if team1.win == 1:
                    coach1team.streak+=1
                else:
                    coach1team.streak=(-1)
            #update coach2 data
            coach2team.wins+=team2.win
            coach2team.losses+=abs(team2.win-1)
            coach2team.forfeit+=team2.forfeit
            if team2.forfeit == 1:
                coach2team.differential+=(-6)
            else:
                coach2team.differential+=team2.diff
            if coach2team.streak < 0:
                if team2.win == 1:
                    coach2team.streak=1
                else:
                    coach2team.streak+=(-1)
            else:
                if team2.win == 1:
                    coach2team.streak+=1
                else:
                    coach2team.streak=(-1)
            #update megas and z
            match.team1megaevolved=team1.megaevolved
            match.team2megaevolved=team2.megaevolved
            match.team1usedz=team1.usedz
            match.team2usedz=team2.usedz
            #save models
            coach1team.save()
            coach2team.save()
            t1pokemon1.save()
            t1pokemon2.save()
            t1pokemon3.save()
            t1pokemon4.save()
            t1pokemon5.save()
            t1pokemon6.save()
            t2pokemon1.save()
            t2pokemon2.save()
            t2pokemon3.save()
            t2pokemon4.save()
            t2pokemon5.save()
            t2pokemon6.save()
            match.save()
            form.save()
            messages.success(request,'Replay has been saved!')
            return  redirect('league_schedule',league_name=league_name)
    return  redirect('league_schedule',league_name=league_name)

def league_match_results(request,league_name,matchid):
    try:
        league_=league.objects.get(name=league_name)
    except:
        return redirect('league_list')
    try:
        match=schedule.objects.get(pk=matchid)
        if match.replay == "Link":
            messages.error(request,f'A replay for that match does not exist!',extra_tags="danger")
            return redirect('league_schedule',league_name=league_name)
    except:
        return redirect('league_schedule',league_name=league_name)
    url=match.replay
    outputstring, team1, team2 = replayparse(url)
    coach1=team1.coach
    coach2=team2.coach 
    coach1alt=showdownalts.objects.get(showdownalt=coach1)
    coach2alt=showdownalts.objects.get(showdownalt=coach2)
    coach1team=coachdata.objects.all().filter(league_name=league_).get(coach=coach1alt.user)
    coach2team=coachdata.objects.all().filter(league_name=league_).get(coach=coach2alt.user)
    context={
        'output': outputstring,
        'team1':team1,
        'team2':team2,
        'team1name':coach1team,
        'team2name':coach2team,
        'replay': url,
        'league_name':league_name,
        'matchid':matchid,
        'showreplay': True,
        'league': league_,
        'leaguepage': True,
    }
    return render(request,"replayanalysisform.html",context)