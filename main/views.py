from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
from django.db.models import Q
from django.core.files.base import ContentFile

import json
from datetime import datetime
import time
import csv
import os
import requests
import math

from accounts.forms import UserRegisterForm
from .models import *
from accounts.models import *
from leagues.models import *
from individualleague.models import *
from pokemonadmin.models import *
from pokemondatabase.models import *
from .forms import HelpForm

from replayanalysis.NewParser.parser import *
from replayanalysis.models import *
from replayanalysis.ShowdownReplayParser.replayparser import *
from replayanalysis.helperfunctions import *
from pokemondraftleague.customdecorators import check_if_clad

def home(request):
    try:
        yourleagues=coachdata.objects.all().filter(Q(coach=request.user)|Q(teammate=request.user))
        if yourleagues.count()>0:
            upcomingmatches=schedule.objects.all().filter(Q(team1__coach=request.user)|Q(team2__coach=request.user)|Q(team1__teammate=request.user)|Q(team2__teammate=request.user)).filter(replay="Link").order_by('duedate','id')[0:4]
            recentresults=schedule.objects.all().filter(Q(team1__coach=request.user)|Q(team2__coach=request.user)|Q(team1__teammate=request.user)|Q(team2__teammate=request.user)).exclude(replay="Link").exclude(Q(team1__coach=request.user)|Q(team1__teammate=request.user),team1alternateattribution__isnull=False).exclude(Q(team2__coach=request.user)|Q(team2__teammate=request.user),team2alternateattribution__isnull=False).order_by('-timestamp','-id')[0:4]
            context = {
                "title": "Pokemon Draft League",
                "yourleagues": yourleagues,
                "upcomingmatches":upcomingmatches,
                "recentresults": recentresults,
            }
            return  render(request,"coachlandingpage.html", context)
    except Exception as e:
        print(e)
    form=UserRegisterForm()
    context = {
        "title": "Pokemon Draft League",
        "form": form,
    }
    return  render(request,"index.html", context)

def about(request):
    coachs=[]
    coachlist=coachdata.objects.all().exclude(league_name__name__contains="Test")
    for c in coachlist:
        if c.coach.username not in coachs:
            coachs.append(c.coach.username)
        if c.teammate and c.teammate.username not in coachs:
            coachs.append(c.teammate.username) 
    coachlist=historical_team.objects.all().exclude(coach1__username="UnclaimedCoach")
    for c in coachlist:
        if c.coach1.username not in coachs:
            coachs.append(c.coach1.username)
        if c.coach2 and c.coach2.username not in coachs:
            coachs.append(c.coach2.username) 
    leagues=league.objects.all().exclude(name__contains="Test")
    historicalmatches=historical_match.objects.all().exclude(replay="").exclude(replay__contains="FF")
    currentmatches=schedule.objects.all().exclude(replay="Link").exclude(replay__contains="FF")
    seasonscompleted=0
    for l in leagues:
        seasonscompleted+=historical_team.objects.all().filter(league=l).distinct('seasonname').count()
    context = {
        "numberofleagues":leagues.count(),
        "uniquecoaches": len(coachs),
        "seasonscompleted":seasonscompleted,
        "matchesplayed": currentmatches.count()+historicalmatches.count(),
    }
    return  render(request,"about.html", context)

def custom404(request,exception):
    return  render(request,"404.html")

def custom500(request,exception):
    return  render(request,"500.html")

def discordbotpage(request):
    return  render(request,"discordbot.html")

def pokemonleaderboard(request):
    leaderboard=pokemon_leaderboard.objects.all().filter(gp__gt=0).order_by('-kills','-differential')
    context = {
        "title": "Pokemon Leaderboard",
        "leaderboard": leaderboard
    }
    return  render(request,"pokemonleaderboard.html",context)

def userleaderboard(request):
    leaderboard=profile.objects.all().filter(Q(wins__gt=0)|Q(losses__gt=0)).order_by('-wins','-differential').exclude(user__username="UnclaimedCoach")
    context = {
        "title": "User Leaderboard",
        "leaderboard": leaderboard
    }
    return  render(request,"userleaderboard.html",context)

def pickemleaderboard(request):
    leaderboard=pickem_leaderboard.objects.all().order_by('-numbercorrect').exclude(matchescompleted__lt=1)
    context = {
        "title": "Pickem Leaderboard",
        "leaderboard": leaderboard
    }
    return  render(request,"pickemleaderboard.html",context)

def replay_database(request):
    database=replaydatabase.objects.all().order_by('team1coach1__username').values('team1coach1__username','team1coach2__username','team2coach1__username','team2coach2__username','winnercoach1__username','winnercoach2__username','replayuser1','replayuser2','winneruser','replay','associatedmatch','associatedhistoricmatch')
    print(database.count())
    database=list(database)
    r=json.dumps(database).replace('null', '""')
    database=json.loads(r)
    context = {
        'database':database,
        'user': request.user.username=="claduva"
    }
    return render(request,"replay_database.html",context)

@login_required
def help(request):
    form=HelpForm(initial={'sender':request.user,'recipient':User.objects.get(username='claduva')})
    if request.method == 'POST':
        form = HelpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your message has been sent! We will get back to you as soon as possible.')
            return redirect('help')
    context = {
        'form': form,
    }
    return render(request,"help.html",context)

def runscript(request): 
    """
    pokemon_moveset.objects.all().delete()
    allmoves=moveinfo.objects.all()
    with open('learnsets.json') as json_file:
        data = json.load(json_file)
        id_=1
        for item in all_pokemon.objects.all():
            print(f'{id_}: {item.pokemon}')
            id_+=1
            name=item.pokemon.lower().replace("-mega-x","").replace("-mega-y","").replace("-mega","").replace("-gmax","").replace(" ","").replace("-","").replace("-y","").replace("-x","").replace(".","").replace(":","").replace("unbound","").replace("primal","").replace("therian","").replace("shayminsky","shaymin")
            name=name.replace('deoxysattack','deoxys').replace('deoxysdefense','deoxys').replace('deoxysspeed','deoxys').replace('origin','').replace('10%','').replace('complete','')
            try:
                ls=data[name]['learnset']
                for move in ls:
                    try:
                        moi=allmoves.get(altname=move)
                        pokemon_moveset.objects.create(pokemon=item,moveinfo=moi)
                    except:
                        print(move)
            except:
                pass
    for item in all_pokemon.objects.all():
        data={}
        data[item.pokemon]={}
        data[item.pokemon]['basestats']={}
        data[item.pokemon]['basestats']['hp']=item.hp
        data[item.pokemon]['basestats']['attack']=item.attack
        data[item.pokemon]['basestats']['defense']=item.defense
        data[item.pokemon]['basestats']['s_attack']=item.s_attack
        data[item.pokemon]['basestats']['s_defense']=item.s_defense
        data[item.pokemon]['basestats']['speed']=item.speed
        data[item.pokemon]['basestats']['bst']=item.bst
        data[item.pokemon]['types']=[]
        for t in item.types.all():
            data[item.pokemon]['types'].append(t.typing)
        data[item.pokemon]['abilities']=[]
        for a in item.abilities.all():
            data[item.pokemon]['abilities'].append(a.ability)
        data[item.pokemon]['learnset']={}
        for move in item.moves.all():
            data[item.pokemon]['learnset'][move.moveinfo.name]={}
            data[item.pokemon]['learnset'][move.moveinfo.name]['Type']=move.moveinfo.move_typing
            data[item.pokemon]['learnset'][move.moveinfo.name]['Category']=move.moveinfo.move_category
            data[item.pokemon]['learnset'][move.moveinfo.name]['Power']=move.moveinfo.move_power
            data[item.pokemon]['learnset'][move.moveinfo.name]['Accuracy']=move.moveinfo.move_accuracy
            data[item.pokemon]['learnset'][move.moveinfo.name]['Priority']=move.moveinfo.move_priority
            data[item.pokemon]['learnset'][move.moveinfo.name]['Secondary Effect']=move.moveinfo.secondary_effect
            data[item.pokemon]['learnset'][move.moveinfo.name]['Secondary Effect Chance']=move.moveinfo.secondary_effect_chance
        data[item.pokemon]['typematchup']={}
        effectiveness=item.effectiveness
        data[item.pokemon]['typematchup']['Bug']=effectiveness.bug
        data[item.pokemon]['typematchup']['Dark']=effectiveness.dark
        data[item.pokemon]['typematchup']['Dragon']=effectiveness.dragon
        data[item.pokemon]['typematchup']['Electric']=effectiveness.electric
        data[item.pokemon]['typematchup']['Fairy']=effectiveness.fairy
        data[item.pokemon]['typematchup']['Fighting']=effectiveness.fighting
        data[item.pokemon]['typematchup']['Fire']=effectiveness.fire
        data[item.pokemon]['typematchup']['Flying']=effectiveness.flying
        data[item.pokemon]['typematchup']['Ghost']=effectiveness.ghost
        data[item.pokemon]['typematchup']['Grass']=effectiveness.grass
        data[item.pokemon]['typematchup']['Ground']=effectiveness.ground
        data[item.pokemon]['typematchup']['Ice']=effectiveness.ice
        data[item.pokemon]['typematchup']['Normal']=effectiveness.normal
        data[item.pokemon]['typematchup']['Poison']=effectiveness.poison
        data[item.pokemon]['typematchup']['Psychic']=effectiveness.psychic
        data[item.pokemon]['typematchup']['Rock']=effectiveness.rock
        data[item.pokemon]['typematchup']['Steel']=effectiveness.steel
        data[item.pokemon]['typematchup']['Water']=effectiveness.water
        data[item.pokemon]['sprites']={}
        sprites=item.sprite
        data[item.pokemon]['sprites']["swsh/ani/standard/PKMN.gif"]=sprites.dexani.url
        data[item.pokemon]['sprites']["swsh/ani/shiny/PKMN.gif"]=sprites.dexanishiny.url
        data[item.pokemon]['sprites']["swsh/png/standard/PKMN.png"]=sprites.dex.url
        data[item.pokemon]['sprites']["swsh/png/shiny/PKMN.png"]=sprites.dexshiny.url
        data[item.pokemon]['sprites']["bw/png/standard/PKMN.png"]=sprites.bw.url
        data[item.pokemon]['sprites']["bw/png/shiny/PKMN.png"]=sprites.bwshiny.url
        data[item.pokemon]['sprites']["afd/png/standard/PKMN.png"]=sprites.afd.url
        data[item.pokemon]['sprites']["afd/png/shiny/PKMN.png"]=sprites.afdshiny.url
        data=json.dumps(data)
        print(item.pokemon)
        item.data=data
        item.save()
        """
    return redirect('home')