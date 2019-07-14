from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
from django.db.models import Q
from django.core.files import File

import json
from datetime import datetime
import time
import csv
import os
import requests

from django.core.files.temp import NamedTemporaryFile

import urllib.request
from PIL import Image

from accounts.forms import UserRegisterForm
from .models import *
from accounts.models import *
from leagues.models import *
from individualleague.models import *
from pokemonadmin.models import *

from replayanalysis.ShowdownReplayParser.replayparser import *
from replayanalysis.helperfunctions import *

# Create your views here.
def home(request):
    try:
        yourleagues=coachdata.objects.all().filter(Q(coach=request.user)|Q(teammate=request.user))
        if yourleagues.count()>0:
            upcomingmatches=schedule.objects.all().filter(Q(team1__coach=request.user)|Q(team2__coach=request.user)|Q(team1__teammate=request.user)|Q(team2__teammate=request.user)).filter(replay="Link")[0:4]
            recentresults=schedule.objects.all().filter(Q(team1__coach=request.user)|Q(team2__coach=request.user)|Q(team1__teammate=request.user)|Q(team2__teammate=request.user)).exclude(replay="Link").order_by('-timestamp','-id')[0:4]
            context = {
                "title": "Pokemon Draft League",
                "yourleagues": yourleagues,
                "upcomingmatches":upcomingmatches,
                "recentresults": recentresults,
            }
            return  render(request,"coachlandingpage.html", context)
    except:
        print("error")
    form=UserRegisterForm()

    context = {
        "title": "Pokemon Draft League",
        "form": form,
    }
    return  render(request,"index.html", context)

def about(request):
    return  render(request,"about.html")

def custom404(request,exception):
    return  render(request,"404.html")

def custom500(request,exception):
    return  render(request,"500.html")

def about(request):
    return  render(request,"about.html")

def pokemonleaderboard(request):
    leaderboard_=all_pokemon.objects.all().order_by('pokemon')
    leaderboard=[]
    for item in leaderboard_:
        rosterson=item.pokemonroster.all()
        for team in rosterson:
            if team.season.league.name.find('Test')==-1:
                item.kills+=team.kills
                item.deaths+=team.deaths
                item.differential+=team.differential
                item.gp+=team.gp
                item.gw+=team.gw
        historicrosterson=item.historicalpokemonroster.all()
        for team in historicrosterson:
            if team.team.league.name.find('Test')==-1:
                item.kills+=team.kills
                item.deaths+=team.deaths
                item.differential+=team.differential
                item.gp+=team.gp
                item.gw+=team.gw
        if item.gp>0:
            leaderboard.append(item)
    leaderboard=sorted(leaderboard, 
                        key=lambda instance: [instance.kills,instance.differential], 
                        reverse=True)
    context = {
        "title": "Pokemon Leaderboard",
        "leaderboard": leaderboard
    }
    return  render(request,"pokemonleaderboard.html",context)

def userleaderboard(request):
    leaderboard_=profile.objects.all()
    leaderboard=[]
    for item in leaderboard_:
        teamscoaching=coachdata.objects.all().filter(Q(coach=item.user)|Q(teammate=item.user))
        for team in teamscoaching:
            if team.league_name.name.find('Test')==-1:
                item.wins+=team.wins
                item.losses+=team.losses
                item.differential+=team.differential
                item.seasonsplayed+=1
        teamscoaching=historical_team.objects.all().filter(Q(coach1=item.user)|Q(coach2=item.user))
        for team in teamscoaching:
            if team.league.name.find('Test')==-1:
                item.wins+=team.wins
                item.losses+=team.losses
                item.differential+=team.differential
                item.seasonsplayed+=1
        if (item.wins+item.losses)>0:
            leaderboard.append(item)
    leaderboard=sorted(leaderboard, 
                        key=lambda instance: [instance.wins,instance.differential], 
                        reverse=True)
    context = {
        "title": "User Leaderboard",
        "leaderboard": leaderboard
    }
    return  render(request,"userleaderboard.html",context)

def pickemleaderboard(request):
    leaderboard_=pickems.objects.all().distinct('user')
    leaderboard=[]
    for item in leaderboard_:
        user_=item.user
        userpickems=user_.pickems.all()
        submitted=userpickems.count()
        correct=userpickems.filter(correct=True).count()
        matchescompleted=userpickems.filter(correct=True).exclude(match__replay='Link').count()
        try:
            percentcorrect=round(correct/matchescompleted*100)
        except:
            percentcorrect=0
        pickemdata={
            'user': user_,
            'submitted':submitted,
            'matchescompleted': matchescompleted,
            'correct':correct,
            'percentcorrect':percentcorrect,
        }
        leaderboard.append(pickemdata)
    leaderboard.sort(
                        key=lambda instance: [instance['percentcorrect'],instance['correct'],instance['submitted']],
                        reverse=True
                        )
    context = {
        "title": "Pickem Leaderboard",
        "leaderboard": leaderboard
    }
    return  render(request,"pickemleaderboard.html",context)

def runscript(request):
    all_leagues=league.objects.all()
    for item in all_leagues:       
        #current seasons
        currentseason=seasonsetting.objects.all().filter(league=item)
        for s in currentseason:
            awardtext=f'{item.name} {s.seasonname}'
            #check finals 
            try:
                awardtogive=award.objects.get(awardname="Champion")
                finalsmatch=schedule.objects.all().filter(season=s).exclude(winner__isnull=True).get(week="Playoffs Finals")
                winner=finalsmatch.winner
                if winner==finalsmatch.team1: runnerup=finalsmatch.team2 
                else: runnerup=finalsmatch.team1
                awardcheck(winner.coach,awardtogive,awardtext)
                if winner.teammate != None:
                    awardcheck(winner.teammate,awardtogive,awardtext)
                awardtogive=award.objects.get(awardname="Runnerup")    
                awardcheck(runnerup.coach,awardtogive,awardtext)
                if runnerup.teammate != None:
                    awardcheck(runnerup.teammate,awardtogive,awardtext)
            except:
                print('Finals not played')
            #check third place
            try:
                awardtogive=award.objects.get(awardname="Thirdplace")
                thirdplacematch=schedule.objects.all().filter(season=s).exclude(winner__isnull=True).get(week="Playoffs Third Place Match")
                winner=thirdplacematch.winner
                awardcheck(winner.coach,awardtogive,awardtext)
                if winner.teammate != None:
                    awardcheck(winner.teammate,awardtogive,awardtext)
            except:
                print('Third place match not played')
            ##check playoffs
            awardtogive=award.objects.get(awardname="Playoffs")
            season_playoffmatches=schedule.objects.all().filter(season=s,week__contains="Playoffs").exclude(winner__isnull=True).distinct('winner')
            for m in season_playoffmatches:
                awardcheck(m.team1.coach,awardtogive,awardtext)
                awardcheck(m.team2.coach,awardtogive,awardtext)
                if m.team1.teammate != None: 
                    awardcheck(m.team1.teammate,awardtogive,awardtext)
                if m.team2.teammate != None: 
                    awardcheck(m.team2.teammate,awardtogive,awardtext)       
        #historical seasons
        historical_seasons=historical_team.objects.all().filter(league=item).distinct('seasonname')
        for s in historical_seasons:
            awardtext=f'{item.name} {s.seasonname}'
            #check finals 
            try:
                awardtogive=award.objects.get(awardname="Champion")
                finalsmatch=historical_match.objects.all().filter(team1__seasonname=s.seasonname).exclude(winner__isnull=True).get(week="Playoffs Finals")
                winner=finalsmatch.winner
                if winner==finalsmatch.team1: runnerup=finalsmatch.team2 
                else: runnerup=finalsmatch.team1
                awardcheck(winner.coach1,awardtogive,awardtext)
                if winner.coach2 != None:
                    awardcheck(winner.coach2,awardtogive,awardtext)
                awardtogive=award.objects.get(awardname="Runnerup")    
                awardcheck(runnerup.coach1,awardtogive,awardtext)
                if runnerup.coach2 != None:
                    awardcheck(runnerup.coach2,awardtogive,awardtext)
            except:
                print('Finals not played')
            #check third place
            try:
                awardtogive=award.objects.get(awardname="Thirdplace")
                thirdplacematch=historical_match.objects.all().filter(team1__seasonname=s.seasonname).exclude(winner__isnull=True).get(week="Playoffs Third Place Match")
                winner=thirdplacematch.winner
                awardcheck(winner.coach1,awardtogive,awardtext)
                if winner.coach2 != None:
                    awardcheck(winner.coach2,awardtogive,awardtext)
            except:
                print('Third place match not played')
            ##check playoffs
            awardtogive=award.objects.get(awardname="Playoffs")
            season_playoffmatches=historical_match.objects.all().filter(team1__seasonname=s.seasonname,week__contains="Playoffs").exclude(winner__isnull=True).distinct('winner')
            awardtext=f'{item.name} {s.seasonname}'
            for m in season_playoffmatches:
                awardcheck(m.team1.coach1,awardtogive,awardtext)
                awardcheck(m.team2.coach1,awardtogive,awardtext)
                if m.team1.coach2 != None: 
                    awardcheck(m.team1.coach2,awardtogive,awardtext)
                if m.team2.coach2 != None: 
                    awardcheck(m.team2.coach2,awardtogive,awardtext)
    return redirect('home')

def awardcheck(coach,awardtogive,awardtext):
    try:
        coachaward.objects.filter(coach=coach, award=awardtogive).get(text=awardtext)
    except:
        coachaward.objects.create(coach=coach,award=awardtogive,text=awardtext)

def findpoke(team1,team2,pokemonname,line_count):
    try:
        item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(pokemon__pokemon=pokemonname)
    except:
        try:
            item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(pokemon__pokemon=f'{pokemonname}-Mega')
        except:
            try:
                item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(pokemon__pokemon=f'{pokemonname}-Mega-X')
            except:
                try:
                    item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(pokemon__pokemon=f'{pokemonname}-Mega-Y')
                except:
                    try:
                        historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(droppedpokemon__pokemon=pokemonname)   
                        item=all_pokemon.objects.all().get(pokemon=pokemonname)
                    except Exception as e:
                        try:
                            historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(droppedpokemon__pokemon=f'{pokemonname}-Mega')   
                            item=all_pokemon.objects.all().get(pokemon=f'{pokemonname}-Mega')
                        except:
                            try:
                                historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(droppedpokemon__pokemon=f'{pokemonname}-Mega-X')   
                                item=all_pokemon.objects.all().get(pokemon=f'{pokemonname}-Mega-X')
                            except:
                                try:
                                    historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).filter(team=team1).get(droppedpokemon__pokemon=f'{pokemonname}-Mega-Y')   
                                    item=all_pokemon.objects.all().get(pokemon=f'{pokemonname}-Mega-Y')
                                except:
                                    try:
                                        historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(droppedpokemon__pokemon=pokemonname)   
                                        item=all_pokemon.objects.all().get(pokemon=pokemonname)
                                    except Exception as e:
                                        try:
                                            historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(droppedpokemon__pokemon=f'{pokemonname}-Mega')   
                                            item=all_pokemon.objects.all().get(pokemon=f'{pokemonname}-Mega')
                                        except:
                                            try:
                                                historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(droppedpokemon__pokemon=f'{pokemonname}-Mega-X')   
                                                item=all_pokemon.objects.all().get(pokemon=f'{pokemonname}-Mega-X')
                                            except:
                                                try:
                                                    historical_freeagency.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(droppedpokemon__pokemon=f'{pokemonname}-Mega-Y')   
                                                    item=all_pokemon.objects.all().get(pokemon=f'{pokemonname}-Mega-Y')
                                                except:
                                                    try:
                                                        item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(pokemon__pokemon=pokemonname)
                                                    except:
                                                        try:
                                                            item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(pokemon__pokemon=f'{pokemonname}-Mega')
                                                        except:
                                                            try:
                                                                item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(pokemon__pokemon=f'{pokemonname}-Mega-X')
                                                            except:
                                                                try:
                                                                    item=historical_roster.objects.all().filter(team__league=team1.league,team__seasonname=team1.seasonname).get(pokemon__pokemon=f'{pokemonname}-Mega-Y')
                                                                except:
                                                                    item=all_pokemon.objects.all().get(pokemon=f'{pokemonname}')
                                                                    print(f'{line_count}. {pokemonname}')                      
    return item