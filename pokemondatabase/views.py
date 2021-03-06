from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q

import json
from datetime import datetime, timedelta,timezone
import time
from background_task import background

from leagues.models import *
from individualleague.models import *
from .models import *
from accounts.forms import UserRegisterForm
from .models import *
from pokemonadmin.models import *
from replayanalysis.models import *
from .forms import *

# Create your views here.
def pokedex(request):
    if request.method=='POST':
        form=Pokedex(request.POST)
        if form.is_valid():
            pokemon_of_interest=form.cleaned_data['pokemon'].pokemon
            return redirect('pokedex_item',pokemon_of_interest=pokemon_of_interest)
    form=Pokedex()
    context = {
        "title": 'Pokemon Info',
        "pokedex": True,
        'form': form,
    }
    return render(request,"pokedex.html", context)

def pokedex_item(request,pokemon_of_interest):
    try:
        pokemon_data=all_pokemon.objects.get(pokemon=pokemon_of_interest)
        draftnumber=draft.objects.all().filter(pokemon=pokemon_data).count()+historical_draft.objects.all().filter(pokemon=pokemon_data).count()
        pokemon_data.timesdrafted+=draftnumber
        roster_data=roster.objects.all().filter(pokemon=pokemon_data).order_by('season__league__name','season__seasonname')
        for item in roster_data:
            pokemon_data.kills+=item.kills
            pokemon_data.deaths+=item.deaths
            pokemon_data.differential+=item.differential
            pokemon_data.gp+=item.gp
            pokemon_data.gw+=item.gw
            pokemon_data.support+=item.support
            pokemon_data.remaininghealth+=item.remaininghealth
            pokemon_data.luck+=item.luck
            pokemon_data.hphealed+=item.hphealed
            pokemon_data.damagedone+=item.damagedone
        otherseason_data=historical_roster.objects.all().filter(pokemon=pokemon_data).order_by('team__league__name','team__seasonname')
        for item in otherseason_data:
            pokemon_data.kills+=item.kills
            pokemon_data.deaths+=item.deaths
            pokemon_data.differential+=item.differential
            pokemon_data.gp+=item.gp
            pokemon_data.gw+=item.gw
            pokemon_data.support+=item.support
            pokemon_data.remaininghealth+=item.remaininghealth
            pokemon_data.luck+=item.luck
            pokemon_data.hphealed+=item.hphealed
            pokemon_data.damagedone+=item.damagedone
    except:
        messages.error(request,'Pokemon does not exist!',extra_tags='danger')
        return redirect('pokedex')
    replays=match_replay.objects.all().filter(Q(data__team1__roster__contains=[{'pokemon':pokemon_of_interest}])|Q(data__team2__roster__contains=[{'pokemon':pokemon_of_interest}])).order_by('match__season__league__name','match__season__seasonname','match__week')
    histreplays=historical_match_replay.objects.all().filter(Q(data__team1__roster__contains=[{'pokemon':pokemon_of_interest}])|Q(data__team2__roster__contains=[{'pokemon':pokemon_of_interest}])).order_by('match__team1__league__name','match__team1__seasonname','match__week')
    context = {
        "title": pokemon_of_interest,
        'pokedexitem': True,
        'pokemon_data':pokemon_data,
        'replays':replays,
        'histreplays':histreplays,
        'roster':roster_data,
        'histroster':otherseason_data,
    }
    return render(request,"pokedex.html", context)

