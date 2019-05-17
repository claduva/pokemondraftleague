from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

import json
from datetime import datetime
import time

from .models import *
from .forms import *
from leagues.models import *
from accounts.models import showdownalts
from pokemondatabase.models import *
from .ShowdownReplayParser.replayparser import *

def checkpokemon(testpokemon,season,team,league_name):
    try:
        pokemon=all_pokemon.objects.get(pokemon=testpokemon)
        rostermon=roster.objects.all().filter(season=season,team=team).get(pokemon=pokemon)
        return rostermon
    except:
        try:
            mega=testpokemon+"-Mega"
            pokemon=all_pokemon.objects.get(pokemon=mega)
            rostermon=roster.objects.all().filter(season=season,team=team).get(pokemon=pokemon)
            return rostermon
        except:
            try:
                mega=testpokemon+"-Mega-X"
                pokemon=all_pokemon.objects.get(pokemon=mega)
                rostermon=roster.objects.all().filter(season=season,team=team).get(pokemon=pokemon)
                return rostermon
            except:
                try:
                    mega=testpokemon+"-Mega-Y"
                    pokemon=all_pokemon.objects.get(pokemon=mega)
                    rostermon=roster.objects.all().filter(season=season,team=team).get(pokemon=pokemon)
                    return rostermon
                except:
                    messages.error(request,f'A match for {testpokemon} could not be found!',extra_tags="danger")
                    return redirect('league_schedule',league_name=league_name)